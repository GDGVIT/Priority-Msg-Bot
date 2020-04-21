logging.info("Long polling unread messages")
updates = self.bot.get_updates()

for update in updates:
    text = update.message.text
    if self.is_event_notification(text):
        event_type = self.extract_event(text)

        logging.info(event_type + " Detected")

        # Incase event type not found
        if event_type is None:
            event_type = 'Some event'
        
        item = self.get_tracker_item(text, event_type)
        self.tracker.append(item)