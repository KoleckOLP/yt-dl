import tempfile

import tempfile

temp_dir = tempfile.TemporaryDirectory()
print(temp_dir.name)

input("press key to delet")

temp_dir.cleanup()