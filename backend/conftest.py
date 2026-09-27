import os
import tempfile

# 必须在导入 app.config 之前指向隔离的数据目录
os.environ.setdefault("DATA_DIR", tempfile.mkdtemp(prefix="curtainlen-test-"))
