class AFMissingFieldError(Exception):
    """
    Custom exception raised when a required field is missing.
    """
    pass


class AFTemplateError(Exception):
    """
    Represents a custom exception for template-related errors.
    """
    pass


class AFMSAError(Exception):
    """
    Represents a custom exception for MSA-related errors.
    """
    pass