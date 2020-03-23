## say goodbye
* goodbye
  - utter_goodbye

## happy event path
* event_notification{"event":"meeting"}
  - utter_event_detected
* affirm
  - event_details_form
  - form{"name": null}
* affirm
  - action_event_submission

## happy path 2

* event_notification{"event":"meeting"}
    - utter_event_detected
* affirm
    - event_details_form
    - form{"name":"event_details_form"}
    - slot{"requested_slot":"event"}
* inform_event{"event":"meeting"}
    - event_details_form
    - slot{"event":"meeting"}
    - slot{"requested_slot":"date"}
* inform_time{"date":"12/12/12"}
    - event_details_form
    - slot{"date":"12/12/12"}
    - slot{"requested_slot":"time"}
* inform_time{"time":"12pm"}
    - event_details_form
    - slot{"time":"12pm"}
    - form{"name":null}
    - slot{"requested_slot":null}
* affirm
    - action_event_submission
