CREATE TABLE IF NOT EXISTS "pt_module" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL DEFAULT '',
  "local_path" TEXT NOT NULL DEFAULT '',
  "code_repo_id" INTEGER NOT NULL DEFAULT 0,
  "spec_repo_id" INTEGER NOT NULL DEFAULT 0
);
