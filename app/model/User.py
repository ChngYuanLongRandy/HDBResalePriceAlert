from .SubUser import SubUser
import itertools


class User(SubUser):
    def __init__(self, id=None, created=None, email=None, verified=None,
                 flatType=None, streetName=None, blkFrom=None, blkTo=None,
                 lastSent=None, token=None):
        SubUser.__init__(self,email=email, flatType=flatType, streetName=streetName,
                       blkFrom=blkFrom, blkTo=blkTo)
        self.id = id
        self.created = created
        self.verified = verified
        self.lastSent = lastSent
        self.token = token

    def __str__(self):
        return f"User(id={self.id}, created={self.created}, email={self.email}, " \
               f"verified={self.verified}, flatType={self.flatType}, " \
               f"streetName={self.streetName}, blkFrom={self.blkFrom}, " \
               f"blkTo={self.blkTo}, lastSent={self.lastSent}, token={self.token})"
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "created": self.created,
            "email": self.email,
            "verified": self.verified,
            "flatType": self.flatType,
            "streetName": self.streetName,
            "blkFrom": self.blkFrom,
            "blkTo": self.blkTo,
            "lastSent": self.lastSent,
            "token": self.token
        }

    def __eq__(self, other):
        """
        Override the equality comparison for Email instances.
        Two instances are considered equal if their email addresses are the same.
        """
        if isinstance(other, User):
            
            return SubUser().__eq__(other)
        
        elif isinstance(other, SubUser):
            return SubUser().__eq__(other)
        
        return False