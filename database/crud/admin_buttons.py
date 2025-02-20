import json
from sqlalchemy.orm import Session
from database.base import AdminButton

def get_admin_buttons(db: Session):
    """Retrieve all admin buttons ordered by position."""
    return db.query(AdminButton).order_by(AdminButton.position).all()

def add_admin_button(db: Session, label: str, action: str, data: dict, prompt: bool):
    """Add a new admin button to the database."""
    try:
        button_data = json.dumps(data) if isinstance(data, dict) else "{}"
        new_button = AdminButton(label=label, action=action, data=button_data, prompt=prompt)

        db.add(new_button)
        db.commit()
        db.refresh(new_button)

        return get_admin_buttons(db)  # Return updated list of buttons
    except Exception as e:
        print(f"❌ Error adding admin button: {e}")
        db.rollback()
        return None

def update_admin_button(db: Session, button_id: int, label: str, action: str, data: dict, prompt: bool):
    """Update an existing admin button in the database."""
    button = db.query(AdminButton).filter(AdminButton.id == button_id).first()
    if not button:
        return None  # Button not found

    try:
        button_data = json.dumps(data) if isinstance(data, dict) else "{}"

        button.label = label
        button.action = action
        button.data = button_data
        button.prompt = prompt

        db.commit()
        db.refresh(button)

        return get_admin_buttons(db)  # Return updated list of buttons
    except Exception as e:
        print(f"❌ Error updating admin button: {e}")
        db.rollback()
        return None

def remove_admin_button(db: Session, button_id: int):
    """Remove an admin button from the database."""
    button = db.query(AdminButton).filter(AdminButton.id == button_id).first()
    if not button:
        return None  # Button not found

    try:
        db.delete(button)
        db.commit()
        return get_admin_buttons(db)  # Return updated list of buttons
    except Exception as e:
        print(f"❌ Error removing admin button: {e}")
        db.rollback()
        return None

def reorder_admin_buttons(db: Session, updated_buttons: list):
    """Update the order of admin buttons."""
    try:
        for button_data in updated_buttons:
            button = db.query(AdminButton).filter(AdminButton.id == button_data["id"]).first()
            if button:
                button.position = button_data["position"]
        db.commit()
        return True
    except Exception as e:
        print(f"❌ Error reordering admin buttons: {e}")
        db.rollback()
        return False
