from tuber import resolve_simple

# create a connection to the running server
# the port number here must match the port used to start the server
client = resolve_simple("localhost:8080")

# access the driver object in the registry as an attribute of the client
driver = client.driver

# Static property: read from the local cache with no network round-trip
print("Model:", driver.MODEL)

# Static property: assignment pushes to the server and updates the local cache
driver.set_MODEL("XR-8000")
print("Model after update:", driver.MODEL)

# Dynamic @property: each read fetches the current value from the server
print("Button:", driver.button)
print("Knob:", driver.knob)

# Dynamic property: assignment pushes the new value to the server
driver.knob = 10
print("Knob after update:", driver.knob)

# set_NAME() is an explicit alternative to assignment for all property types
driver.set_knob(5)
print("Knob via set_knob():", driver.knob)

# Methods work the same as before
driver.push_button()
print("Button after push:", driver.button)

# Note that the return object here is a "TuberResult" object.  This is just a fancy dictionary.
# To return a simple dictionary, pass `convert_json=False` to the resolve_simple() function at the
# top of this script.
print("Driver settings:", driver.get_all())

# Batch several calls in one go — methods and property setters can be mixed.
# set_NAME() inside a context queues a property setter rather than a method call.
# The whole batch is sent as a single packet.
with driver.tuber_context() as ctx:
    ctx.push_button()
    ctx.set_knob(99)
    ctx.set_MODEL("XR-9000")
    ctx.get_all()
    results = ctx()

print("Push button:", results[0])
print("Set knob:", results[1])
print("Set model:", results[2])
print("All settings:", results[3])
print("Model (local cache):", driver.MODEL)  # updated by done-callback
