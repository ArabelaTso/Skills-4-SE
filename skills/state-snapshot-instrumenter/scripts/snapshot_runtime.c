/*
 * Runtime library for capturing state snapshots in C/C++ programs.
 *
 * Compile with: gcc -c snapshot_runtime.c -o snapshot_runtime.o
 * Link with your instrumented program.
 */

#include "snapshot_runtime.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <execinfo.h>
#include <unistd.h>

static FILE* snapshot_file = NULL;
static int snapshot_count = 0;
static int enabled = 1;

void snapshot_init(Snapshot* snapshot, int id, const char* location, const char* type) {
    snapshot->id = id;
    snapshot->location = strdup(location);
    snapshot->type = strdup(type);
    snapshot->variable_count = 0;
    snapshot->variables = NULL;

    // Get timestamp
    time_t now = time(NULL);
    struct tm* tm_info = localtime(&now);
    strftime(snapshot->timestamp, sizeof(snapshot->timestamp), "%Y-%m-%dT%H:%M:%S", tm_info);

    // Capture call stack
    snapshot->stack_depth = backtrace(snapshot->stack_frames, MAX_STACK_DEPTH);
}

void snapshot_add_variable(Snapshot* snapshot, const char* name, void* data, size_t size) {
    if (snapshot->variable_count >= MAX_VARIABLES) {
        return;
    }

    SnapshotVariable* var = &snapshot->variables[snapshot->variable_count++];
    var->name = strdup(name);
    var->size = size;
    var->data = malloc(size);
    memcpy(var->data, data, size);
}

void snapshot_capture(Snapshot* snapshot) {
    if (!enabled) {
        return;
    }

    // Open file if not already open
    if (snapshot_file == NULL) {
        const char* filename = getenv("SNAPSHOT_OUTPUT");
        if (filename == NULL) {
            filename = "snapshots.json";
        }
        snapshot_file = fopen(filename, "w");
        if (snapshot_file == NULL) {
            fprintf(stderr, "Error: Cannot open snapshot file\n");
            return;
        }

        // Write JSON header
        fprintf(snapshot_file, "{\n");
        fprintf(snapshot_file, "  \"format_version\": \"1.0\",\n");
        fprintf(snapshot_file, "  \"language\": \"c\",\n");
        fprintf(snapshot_file, "  \"snapshots\": [\n");
    }

    // Write comma if not first snapshot
    if (snapshot_count > 0) {
        fprintf(snapshot_file, ",\n");
    }

    // Write snapshot as JSON
    fprintf(snapshot_file, "    {\n");
    fprintf(snapshot_file, "      \"snapshot_id\": %d,\n", snapshot->id);
    fprintf(snapshot_file, "      \"timestamp\": \"%s\",\n", snapshot->timestamp);
    fprintf(snapshot_file, "      \"location\": \"%s\",\n", snapshot->location);
    fprintf(snapshot_file, "      \"type\": \"%s\",\n", snapshot->type);

    // Write call stack
    fprintf(snapshot_file, "      \"call_stack\": [\n");
    char** symbols = backtrace_symbols(snapshot->stack_frames, snapshot->stack_depth);
    for (int i = 0; i < snapshot->stack_depth; i++) {
        fprintf(snapshot_file, "        \"%s\"", symbols[i]);
        if (i < snapshot->stack_depth - 1) {
            fprintf(snapshot_file, ",");
        }
        fprintf(snapshot_file, "\n");
    }
    free(symbols);
    fprintf(snapshot_file, "      ],\n");

    // Write variables
    fprintf(snapshot_file, "      \"variables\": {\n");
    for (int i = 0; i < snapshot->variable_count; i++) {
        SnapshotVariable* var = &snapshot->variables[i];
        fprintf(snapshot_file, "        \"%s\": {\n", var->name);
        fprintf(snapshot_file, "          \"size\": %zu,\n", var->size);
        fprintf(snapshot_file, "          \"data\": \"");

        // Write data as hex
        for (size_t j = 0; j < var->size && j < 64; j++) {
            fprintf(snapshot_file, "%02x", ((unsigned char*)var->data)[j]);
        }
        fprintf(snapshot_file, "\"\n");
        fprintf(snapshot_file, "        }");
        if (i < snapshot->variable_count - 1) {
            fprintf(snapshot_file, ",");
        }
        fprintf(snapshot_file, "\n");
    }
    fprintf(snapshot_file, "      }\n");
    fprintf(snapshot_file, "    }");

    fflush(snapshot_file);
    snapshot_count++;
}

void snapshot_free(Snapshot* snapshot) {
    free((void*)snapshot->location);
    free((void*)snapshot->type);

    for (int i = 0; i < snapshot->variable_count; i++) {
        free((void*)snapshot->variables[i].name);
        free(snapshot->variables[i].data);
    }
    free(snapshot->variables);
}

void snapshot_finalize(void) {
    if (snapshot_file != NULL) {
        fprintf(snapshot_file, "\n  ],\n");
        fprintf(snapshot_file, "  \"total_snapshots\": %d\n", snapshot_count);
        fprintf(snapshot_file, "}\n");
        fclose(snapshot_file);
        snapshot_file = NULL;

        fprintf(stderr, "Saved %d snapshots\n", snapshot_count);
    }
}

void snapshot_enable(void) {
    enabled = 1;
}

void snapshot_disable(void) {
    enabled = 0;
}

// Automatic finalization on program exit
__attribute__((destructor))
static void snapshot_cleanup(void) {
    snapshot_finalize();
}
