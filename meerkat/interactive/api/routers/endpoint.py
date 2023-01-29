import logging
from fastapi import HTTPException

from meerkat.errors import TriggerError
from meerkat.interactive.endpoint import Endpoint, endpoint

logger = logging.getLogger(__name__)


@endpoint(prefix="/endpoint", route="/{endpoint}/dispatch/")
def dispatch(
    endpoint: Endpoint,
    payload: dict,
) -> dict:
    """Call an endpoint."""
    logger.debug(f"Dispatching endpoint {endpoint} with payload {payload}.")
    from meerkat.interactive.modification import StoreModification

    # `payload` is a dict with {detail: {key: value} | primitive}
    # Unpack the payload to build the fn_kwargs
    fn_kwargs = {}
    kwargs = payload["detail"]
    if isinstance(kwargs, dict):
        fn_kwargs = kwargs

    try:
        # Run the endpoint
        result, modifications = endpoint.partial(**fn_kwargs).run()
    except TriggerError as e:
        # TODO: handle case where result is not none
        return {"result": None, "modifications": [], "error": str(e)}
    except Exception as e:
        # General exception should be converted to a HTTPException
        # that fastapi can handle.
        from meerkat.state import state
        logger.debug("Exception in dispatch", exc_info=True)
        state.progress_queue.add(None)
        raise HTTPException(status_code=400, detail=str(e)) from e

    # Only return store modifications that are not backend_only
    modifications = [
        m
        for m in modifications
        if not (isinstance(m, StoreModification) and m.backend_only)
    ]

    # Return the modifications and the result to the frontend
    return {"result": result, "modifications": modifications, "error": None}
