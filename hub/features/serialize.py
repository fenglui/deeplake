import copy

from hub.features.features import Primitive, Tensor, FeatureDict


def serialize(input):
    "Converts the input into a serializable format"
    if isinstance(input, Tensor):
        return serialize_tensor(input)
    elif isinstance(input, FeatureDict):
        return serialize_featuredict(input)
    elif isinstance(input, Primitive):
        return serialize_primitive(input)
    else:
        raise TypeError("Unknown type", type(input))


def serialize_tensor(tensor):
    "Converts Tensor and its derivatives into a serializable format"
    d = copy.deepcopy(tensor.__dict__)
    d["type"] = type(tensor).__name__
    if hasattr(tensor, "dtype"):
        d["dtype"] = serialize(tensor.dtype)
    if hasattr(tensor, "class_labels"):
        d["class_labels"] = serialize(tensor.class_labels)
    return d


def serialize_featuredict(fdict):
    "Converts FeatureDict into a serializable format"
    d = {}
    d["type"] = "FeatureDict"
    d["items"] = {}
    for k, v in fdict.__dict__["dict_"].items():
        d["items"][k] = serialize(v)
    return d


def serialize_primitive(primitive):
    "Converts Primitive into a serializable format"
    return str(primitive._dtype)
