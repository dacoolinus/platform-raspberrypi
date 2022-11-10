#include <FreeRTOS.h>
#include <task.h>
#include <queue.h>

volatile QueueHandle_t queue = NULL;
const TickType_t ms_delay = 500 / portTICK_PERIOD_MS;
TaskHandle_t led_task_handle = NULL;

void TaskBlink1(void *unused_arg);

// the setup routine runs once when you press reset:
int main() {
  BaseType_t led_status = xTaskCreate(
    TaskBlink1,
    "Task1",
    256,
    NULL,
    1,
    &led_task_handle
  );

  queue = xQueueCreate(4, sizeof(uint8_t));

  if(led_status == pdPASS) {
  vTaskStartScheduler();
  }

  while(true){
    
  }
}


void TaskBlink1(void *unused_arg){
  uint8_t led_state = 0;
  //pinMode(LED_BUILTIN, OUTPUT);

  while(true){
    led_state = 1;
  //  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    xQueueSendToBack(queue, &led_state, 0);
    vTaskDelay(ms_delay);             // wait for a second
    
    led_state = 0;
  //  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    xQueueSendToBack(queue, &led_state, 0);
    vTaskDelay(ms_delay);             // wait for a second
  }
}
