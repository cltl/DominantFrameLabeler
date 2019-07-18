# Dominant Frame Labeler

The goal of this repository is to exploit Dutch resources to create a Dutch FrameNet

### Prerequisites
Python 3.6 was used to create this project. It might work with older versions of Python.

### Installing


#### Python modules

A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```

#### Resources
A number of GitHub repositories need to be cloned. This can be done calling:
```bash
bash install.sh
```

## How to use
Perform the following call for more information about usage
```
python dominant_frame_labeler.py -h
```

## TODO:
* compare against FrameNet corpus 
* move from predictions to automatically labeling English occurrences
* move from predictions to automatically labeling Dutch and Italian occurrences
* resource-based statistics
* annotate x number of instances
* evaluate

## Authors
* **Marten Postma** (m.c.postma@vu.nl)

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
