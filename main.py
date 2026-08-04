from FunPayAPI import Account
import inspect

print("=" * 50)
print("FunPayAPI DIAGNOSTIC")
print("=" * 50)

print("\nКонструктор Account:")
print(inspect.signature(Account.__init__))

print("\nВсе публичные методы Account:")
for method in dir(Account):
    if not method.startswith("_"):
        print(method)

print("\n" + "=" * 50)
print("END")
print("=" * 50)
