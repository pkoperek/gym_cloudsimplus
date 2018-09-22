from py4j.java_gateway import JavaGateway
import json

gateway = JavaGateway()
simulation_environment = gateway.entry_point

# result = simulation_environment.step(0)

# print(result)
# print(result.isDone())
# print(result.getObs())
# print(result.getReward())

result = simulation_environment.render()
result = json.loads(result)

print("Start: " + str(result[0][-5:]))

#print("Size: " + str(len(result)))
#for i in range(len(result)):
#    print("Render: " + str(i) + " " + str(len(result[i])))
#
#    for j in range(len(result[i])):
#        print("Render: " + str(i) + " " + str(j) + " " + str(result[i][j]))


simulation_environment.step(0)
result = simulation_environment.render()
result = json.loads(result)

print("Did nothing: " + str(result[0][-5:]))

simulation_environment.step(1)
result = simulation_environment.render()
result = json.loads(result)
print("Added VM: " + str(result[0][-5:]))

simulation_environment.step(0)
result = simulation_environment.render()
result = json.loads(result)
print("Did nothing: " + str(result[0][-5:]))

simulation_environment.step(2)
result = simulation_environment.render()
result = json.loads(result)
print("Destroyed VM: " + str(result[0][-5:]))

simulation_environment.step(0)
result = simulation_environment.render()
result = json.loads(result)
print("Did nothing: " + str(result[0][-5:]))
simulation_environment.step(0)
result = simulation_environment.render()
result = json.loads(result)
print("Did nothing: " + str(result[0][-5:]))
simulation_environment.step(0)
result = simulation_environment.render()
result = json.loads(result)
print("Did nothing: " + str(result[0][-5:]))
