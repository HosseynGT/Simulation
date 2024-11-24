import simpy
import random


def hospital_simulation():
    # Create the environment
    env = simpy.Environment()
    
    # Define resources
    prep_rooms = simpy.Resource(env, 3)  # 3 preparation rooms
    op_theater = simpy.Resource(env, 1)  # 1 operating theater
    recovery_rooms = simpy.Resource(env, 3)  # 3 recovery rooms
    
    # Define average times (in minutes)
    prep_time = 40
    op_time = 20
    recovery_time = 40
    

    def patient_generator():
        patient_id = 0
        while True:
            # Random service times (exponentially distributed)
            prep = random.expovariate(1 / prep_time)
            op = random.expovariate(1 / op_time)
            recovery = random.expovariate(1 / recovery_time)
            

            print(f"Patient {patient_id} arrives at {env.now:.2f} with prep time {prep:.2f}, "
                  f"operation time {op:.2f}, recovery time {recovery:.2f}")
            
            # Create a patient process
            env.process(patient_process(patient_id, prep, op, recovery))

            patient_id += 1
            yield env.timeout(random.expovariate(0.04))  # Arrival rate of 0.04 patients per minute
    

    def patient_process(patient_id, prep, op, recovery):
        # Preparation Phase
        with prep_rooms.request() as req:
            yield req
            print(f"Patient {patient_id} starts preparation at {env.now:.2f}")
            yield env.timeout(prep)
            print(f"Patient {patient_id} finishes preparation at {env.now:.2f}")
        
        # Operation Phase
        with op_theater.request() as req:
            yield req
            print(f"Patient {patient_id} starts operation at {env.now:.2f}")
            yield env.timeout(op)
            print(f"Patient {patient_id} finishes operation at {env.now:.2f}")
        
        # Recovery Phase
        with recovery_rooms.request() as req:
            yield req
            print(f"Patient {patient_id} starts recovery at {env.now:.2f}")
            yield env.timeout(recovery)
            print(f"Patient {patient_id} finishes recovery at {env.now:.2f}")
    

    def monitor():
        while True:
            print(f"At time {env.now:.2f}:")
            print(f"  Preparation room queue = {len(prep_rooms.queue)}")
            print(f"  Operating Theater queue = {len(op_theater.queue)}")
            print(f"  Recovery room queue = {len(recovery_rooms.queue)}")
            yield env.timeout(5)  # Monitor every 5 minutes
    

    env.process(patient_generator())
    env.process(monitor())
    
    # Run the simulation for 500 minutes
    env.run(until=500)


hospital_simulation()
