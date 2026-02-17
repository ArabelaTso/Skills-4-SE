/*
 * Header file for snapshot runtime library.
 */

#ifndef SNAPSHOT_RUNTIME_H
#define SNAPSHOT_RUNTIME_H

#include <stddef.h>

#define MAX_VARIABLES 100
#define MAX_STACK_DEPTH 50

typedef struct {
    const char* name;
    void* data;
    size_t size;
} SnapshotVariable;

typedef struct {
    int id;
    const char* location;
    const char* type;
    char timestamp[32];
    void* stack_frames[MAX_STACK_DEPTH];
    int stack_depth;
    SnapshotVariable* variables;
    int variable_count;
} Snapshot;

// Initialize a snapshot
void snapshot_init(Snapshot* snapshot, int id, const char* location, const char* type);

// Add a variable to the snapshot
void snapshot_add_variable(Snapshot* snapshot, const char* name, void* data, size_t size);

// Capture and save the snapshot
void snapshot_capture(Snapshot* snapshot);

// Free snapshot resources
void snapshot_free(Snapshot* snapshot);

// Finalize and close snapshot file
void snapshot_finalize(void);

// Enable/disable snapshot capture
void snapshot_enable(void);
void snapshot_disable(void);

// Convenience macro for manual snapshots
#define __SNAPSHOT__(location) \
    do { \
        Snapshot __snap; \
        snapshot_init(&__snap, __LINE__, location, "manual"); \
        snapshot_capture(&__snap); \
        snapshot_free(&__snap); \
    } while(0)

#endif // SNAPSHOT_RUNTIME_H
