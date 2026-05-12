from django.db import models
from accounts.models import User
from elections.models import Election, Candidate
import uuid

class Vote(models.Model):
    """Anonymous vote storage linked only by a secure SHA-256 hash."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vote_hash = models.CharField(max_length=64, unique=True, default="")
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    cast_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote {self.vote_hash[:8]} in {self.election.title}"

class VoteRecord(models.Model):
    """Records which elections a user has voted in (for profile display) without linking to their candidate choice."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_records')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='vote_records')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vote_records'
        unique_together = ('user', 'election')
