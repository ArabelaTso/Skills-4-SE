package snapshot;

import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * Runtime library for capturing state snapshots in Java programs.
 */
public class SnapshotRuntime {
    private static List<Snapshot> snapshots = new ArrayList<>();
    private static String outputFile = System.getenv().getOrDefault("SNAPSHOT_OUTPUT", "snapshots.json");
    private static boolean enabled = true;

    static {
        // Register shutdown hook to save snapshots
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            saveSnapshots();
        }));
    }

    public static class Snapshot {
        public int id;
        public String timestamp;
        public String location;
        public String type;
        public List<String> callStack;
        public Map<String, Object> variables;

        public Snapshot(int id, String location, String type) {
            this.id = id;
            this.location = location;
            this.type = type;
            this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            this.callStack = new ArrayList<>();
            this.variables = new HashMap<>();
        }
    }

    public static void captureSnapshot(int id, String location, String type) {
        if (!enabled) {
            return;
        }

        Snapshot snapshot = new Snapshot(id, location, type);

        // Capture call stack
        StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
        for (int i = 2; i < stackTrace.length; i++) {  // Skip getStackTrace and captureSnapshot
            StackTraceElement element = stackTrace[i];
            snapshot.callStack.add(String.format("%s.%s(%s:%d)",
                element.getClassName(),
                element.getMethodName(),
                element.getFileName(),
                element.getLineNumber()));
        }

        snapshots.add(snapshot);
    }

    public static void addVariable(String name, Object value) {
        if (!snapshots.isEmpty()) {
            Snapshot lastSnapshot = snapshots.get(snapshots.size() - 1);
            lastSnapshot.variables.put(name, serializeValue(value));
        }
    }

    private static Object serializeValue(Object value) {
        if (value == null) {
            return null;
        }

        // Handle primitives and strings
        if (value instanceof String || value instanceof Number || value instanceof Boolean) {
            return value;
        }

        // Handle arrays
        if (value.getClass().isArray()) {
            List<Object> list = new ArrayList<>();
            int length = Math.min(java.lang.reflect.Array.getLength(value), 100);
            for (int i = 0; i < length; i++) {
                list.add(serializeValue(java.lang.reflect.Array.get(value, i)));
            }
            return list;
        }

        // Handle collections
        if (value instanceof Collection) {
            List<Object> list = new ArrayList<>();
            int count = 0;
            for (Object item : (Collection<?>) value) {
                if (count++ >= 100) break;
                list.add(serializeValue(item));
            }
            return list;
        }

        if (value instanceof Map) {
            Map<String, Object> map = new HashMap<>();
            int count = 0;
            for (Map.Entry<?, ?> entry : ((Map<?, ?>) value).entrySet()) {
                if (count++ >= 100) break;
                map.put(String.valueOf(entry.getKey()), serializeValue(entry.getValue()));
            }
            return map;
        }

        // For other objects, return type and toString
        Map<String, Object> obj = new HashMap<>();
        obj.put("__type__", value.getClass().getName());
        obj.put("__repr__", value.toString());
        return obj;
    }

    public static void saveSnapshots() {
        if (snapshots.isEmpty()) {
            return;
        }

        try (PrintWriter writer = new PrintWriter(new FileWriter(outputFile))) {
            writer.println("{");
            writer.println("  \"format_version\": \"1.0\",");
            writer.println("  \"language\": \"java\",");
            writer.println("  \"total_snapshots\": " + snapshots.size() + ",");
            writer.println("  \"snapshots\": [");

            for (int i = 0; i < snapshots.size(); i++) {
                Snapshot snapshot = snapshots.get(i);
                writer.println("    {");
                writer.println("      \"snapshot_id\": " + snapshot.id + ",");
                writer.println("      \"timestamp\": \"" + snapshot.timestamp + "\",");
                writer.println("      \"location\": \"" + snapshot.location + "\",");
                writer.println("      \"type\": \"" + snapshot.type + "\",");

                // Write call stack
                writer.println("      \"call_stack\": [");
                for (int j = 0; j < snapshot.callStack.size(); j++) {
                    writer.print("        \"" + snapshot.callStack.get(j) + "\"");
                    if (j < snapshot.callStack.size() - 1) {
                        writer.println(",");
                    } else {
                        writer.println();
                    }
                }
                writer.println("      ],");

                // Write variables
                writer.println("      \"variables\": {");
                int varCount = 0;
                for (Map.Entry<String, Object> entry : snapshot.variables.entrySet()) {
                    writer.print("        \"" + entry.getKey() + "\": " + toJson(entry.getValue()));
                    if (++varCount < snapshot.variables.size()) {
                        writer.println(",");
                    } else {
                        writer.println();
                    }
                }
                writer.println("      }");

                writer.print("    }");
                if (i < snapshots.size() - 1) {
                    writer.println(",");
                } else {
                    writer.println();
                }
            }

            writer.println("  ]");
            writer.println("}");

            System.err.println("Saved " + snapshots.size() + " snapshots to " + outputFile);
        } catch (IOException e) {
            System.err.println("Error saving snapshots: " + e.getMessage());
        }
    }

    private static String toJson(Object value) {
        if (value == null) {
            return "null";
        }
        if (value instanceof String) {
            return "\"" + value.toString().replace("\"", "\\\"") + "\"";
        }
        if (value instanceof Number || value instanceof Boolean) {
            return value.toString();
        }
        if (value instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            List<?> list = (List<?>) value;
            for (int i = 0; i < list.size(); i++) {
                sb.append(toJson(list.get(i)));
                if (i < list.size() - 1) sb.append(", ");
            }
            sb.append("]");
            return sb.toString();
        }
        if (value instanceof Map) {
            StringBuilder sb = new StringBuilder("{");
            Map<?, ?> map = (Map<?, ?>) value;
            int count = 0;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                if (count++ > 0) sb.append(", ");
                sb.append("\"").append(entry.getKey()).append("\": ").append(toJson(entry.getValue()));
            }
            sb.append("}");
            return sb.toString();
        }
        return "\"" + value.toString().replace("\"", "\\\"") + "\"";
    }

    public static void enable() {
        enabled = true;
    }

    public static void disable() {
        enabled = false;
    }

    public static void setOutputFile(String filename) {
        outputFile = filename;
    }
}
