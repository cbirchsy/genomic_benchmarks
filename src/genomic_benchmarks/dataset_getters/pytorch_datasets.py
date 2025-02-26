from genomic_benchmarks.data_check import is_downloaded
from genomic_benchmarks.loc2seq import download_dataset
from genomic_benchmarks.utils.paths import CACHE_PATH
from torch.utils.data import Dataset


class GenomicClfDataset(Dataset):
    """
    A class to represent generic genomic classification pytorch dataset.
    Instance of this class can be directly wrapped by pytorch DataLoader
    """

    def __init__(self, dset_name, split, dest_path=CACHE_PATH, force_download=False, version=None, use_cloud_cache=True):
        """
        Parameters
            dset_name : str
                One of the existing dataset names, list available at TODO
            split : str
                train' or 'test'
            force_download : bool
                Whether to re-download already existing files
            version : int
                Version of the dataset
            use_cloud_cache : bool
                Whether to use the cloud cache for downloading the dataset
        """
        base_path = dest_path / dset_name

        if not is_downloaded(dset_name, dest_path=dest_path) or force_download:
            download_dataset(dset_name, version=version, dest_path=dest_path, force_download=force_download, use_cloud_cache=use_cloud_cache)

        if split == "train" or split == "test":
            base_path = base_path / split
        else:
            raise Exception("Define split, train or test")

        self.all_paths = []
        self.all_labels = []
        label_mapper = {}

        for i, x in enumerate(base_path.iterdir()):
            label_mapper[x.stem] = i

        for label_type in label_mapper.keys():
            for x in (base_path / label_type).iterdir():
                self.all_paths.append(x)
                self.all_labels.append(label_mapper[label_type])

    def __len__(self):
        return len(self.all_paths)

    def __getitem__(self, idx):
        txt_path = self.all_paths[idx]
        with open(txt_path, "r") as f:
            content = f.read()
        x = content
        y = self.all_labels[idx]
        return x, y


def get_dataset(dataset_name, split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset(dataset_name, split, force_download, version, use_cloud_cache)


def DemoCodingVsIntergenomicSeqs(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("demo_coding_vs_intergenomic_seqs", split, force_download, version, use_cloud_cache)


def DemoHumanOrWorm(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("demo_human_or_worm", split, force_download, version, use_cloud_cache)


def DrosophilaEnhancersStark(split, force_download=False, version=None):
    return GenomicClfDataset("drosophila_enhancers_stark", split, force_download, version)


def DemoMouseEnhancers(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("dummy_mouse_enhancers_ensembl", split, force_download, version, use_cloud_cache)


def HumanEnhancersCohn(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("human_enhancers_cohn", split, force_download, version, use_cloud_cache)


def HumanEnhancersEnsembl(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("human_enhancers_ensembl", split, force_download, version, use_cloud_cache)


def HumanNontataPromoters(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("human_nontata_promoters", split, force_download, version, use_cloud_cache)


def HumanOcrEnsembl(split, force_download=False, version=None, use_cloud_cache=True):
    return GenomicClfDataset("human_ocr_ensembl", split, force_download, version, use_cloud_cache)
