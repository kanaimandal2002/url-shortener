from datetime import datetime

class ShortenedURL:
    def __init__(self, short_code, original_url, created_at=None, click_count=0):
        self.short_code = short_code
        self.original_url = original_url
        self.created_at = created_at if created_at else datetime.now()
        self.click_count = click_count
