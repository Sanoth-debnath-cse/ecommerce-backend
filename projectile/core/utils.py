def get_slug_full_name(instance):
    if instance.first_name:
        return f"{instance.first_name} {instance.last_name}".strip()
    else:
        return f"{instance.phone}".strip()
