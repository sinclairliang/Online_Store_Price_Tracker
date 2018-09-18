from src.models.alerts.alert import Alert

alerts_need_updates = Alert.find_update()
# Then I have a list of items that needed update

for alert in alerts_need_updates:
    alert.load_item_price()
    alert.send_email_if_price_reached()
