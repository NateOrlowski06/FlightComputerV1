import time
from Altimeter import Altimeter
from DataLogger import DataLogger
from Accelerometer import Accelerometer
from StateMachine import StateMachine
import os

"""
This is where the sensors are initialized, the main loop runs, 
and where the timing of events is handled
"""

def main():

    altimeter = Altimeter()
    data_logger = DataLogger()
    accelerometer = Accelerometer()
    state_machine = StateMachine()

    state_dt = 0.1 #The time interval that the state is updated
    sensor_dt = 0.04 #Time interval that sensors are updated based on max polling rate for BMP180
    
    state_update_initial_time = time.time()
    sensor_update_initial_time = time.time()
   


    while(str(state_machine.getState()) != "RocketState.LANDED"):
        """
        The sensors are updated 10 times as fast as the state is checked. 
        The data is added to a moving average that is 10 datapoints wide that is updated every sensor_dt
        The state is checked every state_dt and data is logged 
        """

        current_time = time.time()
        
        if(current_time - sensor_update_initial_time >= sensor_dt):
            altimeter.update(sensor_dt) 
            accelerometer.update()
            sensor_update_initial_time = time.time()

        if(current_time - state_update_initial_time >= state_dt):
            state_machine.update(altimeter,
                                 accelerometer,
                                 data_logger, 
                                 current_time)
            state_update_initial_time = time.time()

    time.sleep(5)
    os.system("sudo shutdown -h now")
    
if __name__ == "__main__":
    main()    











