//  This source code is licensed under both the GPLv2 (found in the
//  Copyright (c) 2011-present, Facebook, Inc.  All rights reserved.
//  COPYING file in the root directory) and Apache 2.0 License
//  (found in the LICENSE.Apache file in the root directory).
//
// Copyright (c) 2011 The LevelDB Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file. See the AUTHORS file for names of contributors.


#include "rocksdb/c.h"

#include <cstdlib>
#include <map>
#include <unordered_set>
#include <vector>

//#include "port/port.h"
#include "rocksdb/cache.h"
#include "rocksdb/compaction_filter.h"
#include "rocksdb/comparator.h"
#include "rocksdb/convenience.h"
#include "rocksdb/db.h"
#include "rocksdb/env.h"
#include "rocksdb/filter_policy.h"
#include "rocksdb/iterator.h"
#include "rocksdb/memtablerep.h"
#include "rocksdb/merge_operator.h"
#include "rocksdb/options.h"
#include "rocksdb/perf_context.h"
#include "rocksdb/rate_limiter.h"
#include "rocksdb/slice_transform.h"
#include "rocksdb/statistics.h"
#include "rocksdb/status.h"
#include "rocksdb/table.h"
#include "rocksdb/universal_compaction.h"
#include "rocksdb/utilities/backup_engine.h"
#include "rocksdb/utilities/checkpoint.h"
#include "rocksdb/utilities/db_ttl.h"
#include "rocksdb/utilities/memory_util.h"
#include "rocksdb/utilities/optimistic_transaction_db.h"
#include "rocksdb/utilities/table_properties_collectors.h"
#include "rocksdb/utilities/transaction.h"
#include "rocksdb/utilities/transaction_db.h"
#include "rocksdb/utilities/write_batch_with_index.h"
#include "rocksdb/write_batch.h"
//#include "utilities/merge_operators.h"

using ROCKSDB_NAMESPACE::BackupEngine;
using ROCKSDB_NAMESPACE::BackupEngineOptions;
using ROCKSDB_NAMESPACE::BackupID;
using ROCKSDB_NAMESPACE::BackupInfo;
using ROCKSDB_NAMESPACE::BatchResult;
using ROCKSDB_NAMESPACE::BlockBasedTableOptions;
using ROCKSDB_NAMESPACE::BottommostLevelCompaction;
using ROCKSDB_NAMESPACE::BytewiseComparator;
using ROCKSDB_NAMESPACE::Cache;
using ROCKSDB_NAMESPACE::Checkpoint;
using ROCKSDB_NAMESPACE::ColumnFamilyDescriptor;
using ROCKSDB_NAMESPACE::ColumnFamilyHandle;
using ROCKSDB_NAMESPACE::ColumnFamilyOptions;
using ROCKSDB_NAMESPACE::CompactionFilter;
using ROCKSDB_NAMESPACE::CompactionFilterFactory;
using ROCKSDB_NAMESPACE::CompactionOptionsFIFO;
using ROCKSDB_NAMESPACE::CompactRangeOptions;
using ROCKSDB_NAMESPACE::Comparator;
using ROCKSDB_NAMESPACE::CompressionType;
using ROCKSDB_NAMESPACE::CuckooTableOptions;
using ROCKSDB_NAMESPACE::DB;
using ROCKSDB_NAMESPACE::DBOptions;
using ROCKSDB_NAMESPACE::DbPath;
using ROCKSDB_NAMESPACE::Env;
using ROCKSDB_NAMESPACE::EnvOptions;
using ROCKSDB_NAMESPACE::FileLock;
using ROCKSDB_NAMESPACE::FilterPolicy;
using ROCKSDB_NAMESPACE::FlushOptions;
using ROCKSDB_NAMESPACE::InfoLogLevel;
using ROCKSDB_NAMESPACE::IngestExternalFileOptions;
using ROCKSDB_NAMESPACE::Iterator;
using ROCKSDB_NAMESPACE::LiveFileMetaData;
using ROCKSDB_NAMESPACE::Logger;
using ROCKSDB_NAMESPACE::LRUCacheOptions;
using ROCKSDB_NAMESPACE::MemoryAllocator;
using ROCKSDB_NAMESPACE::MemoryUtil;
using ROCKSDB_NAMESPACE::MergeOperator;
using ROCKSDB_NAMESPACE::NewBloomFilterPolicy;
using ROCKSDB_NAMESPACE::NewCompactOnDeletionCollectorFactory;
using ROCKSDB_NAMESPACE::NewGenericRateLimiter;
using ROCKSDB_NAMESPACE::NewLRUCache;
using ROCKSDB_NAMESPACE::NewRibbonFilterPolicy;
using ROCKSDB_NAMESPACE::OptimisticTransactionDB;
using ROCKSDB_NAMESPACE::OptimisticTransactionOptions;
using ROCKSDB_NAMESPACE::Options;
using ROCKSDB_NAMESPACE::PerfContext;
using ROCKSDB_NAMESPACE::PerfLevel;
using ROCKSDB_NAMESPACE::PinnableSlice;
using ROCKSDB_NAMESPACE::RandomAccessFile;
using ROCKSDB_NAMESPACE::Range;
using ROCKSDB_NAMESPACE::RateLimiter;
using ROCKSDB_NAMESPACE::ReadOptions;
using ROCKSDB_NAMESPACE::RestoreOptions;
using ROCKSDB_NAMESPACE::SequentialFile;
using ROCKSDB_NAMESPACE::Slice;
using ROCKSDB_NAMESPACE::SliceParts;
using ROCKSDB_NAMESPACE::SliceTransform;
using ROCKSDB_NAMESPACE::Snapshot;
using ROCKSDB_NAMESPACE::SstFileWriter;
using ROCKSDB_NAMESPACE::Status;
using ROCKSDB_NAMESPACE::TablePropertiesCollectorFactory;
using ROCKSDB_NAMESPACE::Transaction;
using ROCKSDB_NAMESPACE::TransactionDB;
using ROCKSDB_NAMESPACE::TransactionDBOptions;
using ROCKSDB_NAMESPACE::TransactionLogIterator;
using ROCKSDB_NAMESPACE::TransactionOptions;
using ROCKSDB_NAMESPACE::WALRecoveryMode;
using ROCKSDB_NAMESPACE::WritableFile;
using ROCKSDB_NAMESPACE::WriteBatch;
using ROCKSDB_NAMESPACE::WriteBatchWithIndex;
using ROCKSDB_NAMESPACE::WriteOptions;

using std::vector;
using std::unordered_set;

struct rocksdb_t                 { DB*               rep; };
struct rocksdb_column_family_handle_t  { ColumnFamilyHandle* rep; };

int rocksdb_property_int(
    rocksdb_t* db,
    const char* propname,
    uint64_t *out_val) {
  if (db->rep->GetIntProperty(Slice(propname), out_val)) {
    return 0;
  } else {
    return -1;
  }
}

int rocksdb_property_int_cf(
    rocksdb_t* db,
    rocksdb_column_family_handle_t* column_family,
    const char* propname,
    uint64_t *out_val) {
  if (db->rep->GetIntProperty(column_family->rep, Slice(propname), out_val)) {
    return 0;
  } else {
    return -1;
  }
}

