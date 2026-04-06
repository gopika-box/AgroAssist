from django.db import models
from accounts.models import User
from marketplace.models import MarketplaceItem

class FarmerDoubt(models.Model):
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doubts_asked",
        limit_choices_to={'role': 'farmer'}
    )

    officer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doubts_received",
        limit_choices_to={'role': 'officer'}
    )

    panchayat = models.CharField(max_length=50)

    question = models.TextField()
    reply = models.TextField(blank=True, null=True)

    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Doubt by {self.farmer.username}"

class ChatRoom(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_chats"
    )
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="farmer_chats"
    )
    item = models.ForeignKey(
        MarketplaceItem,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat: {self.customer.username} ↔ {self.farmer.username}"


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:20]}"
    
class BlockList(models.Model):
    blocker = models.ForeignKey(User, related_name='blocking', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(User, related_name='blocked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a farmer can't block the same customer twice in the DB
        unique_together = ('blocker', 'blocked_user')

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked_user}"