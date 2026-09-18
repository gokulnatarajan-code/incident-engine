from log_writer import emit
import time


def trigger_db_failure():
	emit("database", "ERROR", "connection pool exhausted, max_connections=20 reached")
	for i in range(40):
		emit("api", "ERROR", f"upstream timeout calling database (attempt {i})")
	for i in range(60):
		emit("frontend", "WARN", f"slow response from /api/orders ({800+i*10}ms)")


if __name__ == "__main__":
	print("Triggering chaos...")
	trigger_db_failure()
	print("Done. Check logs/all.log")
