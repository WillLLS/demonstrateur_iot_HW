/***
 * @author William Lalis
 * @date 2022/10/23
*/
#include "config.h"

#include "sensor.h"
#include "log.h"
#include "wifi.h"

void init();

/**
 * @brief Main task
*/
void app_main(void)
{
    init();

    while(1){

        vTaskDelay(1);
    }
}


/**
 * @brief Initiate the FreeRTOS Tasks and Queues 
*/
void init(){
    
    flagStart = 0;
    init_smart_wifi();

    while(!flagStart){
        vTaskDelay(1);
    }
    
    
    
    QueueHeart          = xQueueCreate(2, sizeof(char[2]));
    QueueBreath         = xQueueCreate(2, sizeof(char[2]));
    QueueHumanPSE       = xQueueCreate(2, sizeof(char[5]));

    xTaskCreate(monitoring, "Log task", 2048, NULL, 10, NULL);
    xTaskCreate(sensor_task, "Read Sensor", 4096, NULL, 10, NULL);
}  
