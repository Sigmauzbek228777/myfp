from FunPayAPI import Account
import inspect

print("=== Account.__init__ ===")
print(inspect.signature(Account.__init__))

print("\n=== Методы Account ===")
for method in dir(Account):
    if not method.startswith("_"):
        print(method)
