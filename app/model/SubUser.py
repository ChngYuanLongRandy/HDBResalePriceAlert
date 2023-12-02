class SubUser:
    def __init__(self, email=None, 
                 flatType=None, streetName=None, blkFrom=None, blkTo=None):

        self.email = email
        self.flatType = flatType
        self.streetName = streetName
        self.blkFrom = int(blkFrom)
        self.blkTo = int(blkTo)

    def __str__(self):
        return f"SubUser(email={self.email}, " \
               f"flatType={self.flatType}, " \
               f"streetName={self.streetName}, blkFrom={self.blkFrom}, " \
               f"blkTo={self.blkTo})"

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            "email": self.email,
            "flatType": self.flatType,
            "streetName": self.streetName,
            "blkFrom": self.blkFrom,
            "blkTo": self.blkTo,
        }

    
    def __eq__(self, other):
        """
        Override the equality comparison for SubUser instances.
        Two instances are considered equal if their specified attributes are the same.
        """
        if isinstance(other, SubUser):
            return (
                other.email == self.email and
                other.blkFrom == self.blkFrom and
                other.blkTo == self.blkTo and
                other.streetName == self.streetName and
                other.flatType == self.flatType
            )
        return False