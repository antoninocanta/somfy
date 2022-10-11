import logging
import exceptions
import json

def filter_devices(Data):
    logging.debug("start filter devices")

    if (not "uiClass" in json.dumps(Data)):
        logging.error("filter_devices: missing uiClass in response")
        logging.debug(str(Data))
        return

    filtered_devices = list()
    for device in Data:
        logging.debug("filter_devices: Device name: "+device["label"]+" Device class: "+device["definition"]["uiClass"])
        if (((device["definition"]["uiClass"] == "RollerShutter") 
            or (device["definition"]["uiClass"] == "LightSensor") 
            or (device["definition"]["uiClass"] == "ExteriorScreen") 
            or (device["definition"]["uiClass"] == "Screen") 
            or (device["definition"]["uiClass"] == "Awning") 
            or (device["definition"]["uiClass"] == "Pergola") 
            or (device["definition"]["uiClass"] == "GarageDoor") 
            or (device["definition"]["uiClass"] == "Window") 
            or (device["definition"]["uiClass"] == "VenetianBlind") 
            or (device["definition"]["uiClass"] == "ExteriorVenetianBlind")) 
            and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
            logging.debug("filter_devices: type of device = "+str(type(device)))
            filtered_devices.append(device)
            logging.info("supported device found: "+ str(device))
        else:
            logging.debug("unsupported device found: "+ str(device))

    logging.debug("finished filter devices")
    return filtered_devices

def handle_response(response, action):
    """handle faulty responses"""
    if response.status_code >= 300 and response.status_code < 400:
        logging.error("status code " + str(response.status_code) + " this is likely a bug")
        raise exceptions.TahomaException("failed request during "+ action + ": " + str(response.status_code))
    elif response.status_code == 400:
        logging.error("status code " + str(response.status_code) + " this is a bug, bad request made, url or body needs to be checked")
        raise exceptions.TahomaException("failed request during "+ action + ", check url or body: " + str(response.status_code))
    elif response.status_code == 401:
        logging.error("status code " + str(response.status_code) + " authorisation failed, check credentials")
        raise exceptions.TahomaException("failed request during "+ action + ", check credentials: " + str(response.status_code))
    elif response.status_code == 404:
        logging.error("status code " + str(response.status_code) + " server not found")
        raise exceptions.TahomaException("failed request during "+ action + ", server not found: " + str(response.status_code))
    elif response.status_code >= 500:
        logging.error("status code " + str(response.status_code) + " a server sided problem")
        raise exceptions.TahomaException("failed request during "+ action + ": " + str(response.status_code))
    else:
        logging.error("status code " + str(response.status_code))
        raise exceptions.TahomaException("failed request during "+ action + ": " + str(response.status_code))        
    return
