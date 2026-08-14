import io
from stillpoint import stillpoint
from stillpoint.typography import aligned_count, percent, elapsed
from stillpoint.color import Gradient


def test_iterates_all_items():
    out = io.StringIO()
    items = list(stillpoint(range(10), label="test", stream=out))
    assert items == list(range(10))


def test_infers_total_from_len():
    out = io.StringIO()
    list(stillpoint([1, 2, 3], stream=out))
    assert "3" in out.getvalue()


def test_typography_alignment():
    assert aligned_count(5, 100).endswith("100")
    assert percent(50, 100).strip() == "50%"
    assert elapsed(65) == "1:05"


def test_gradient_endpoints():
    g = Gradient(["#000000", "#ffffff"])
    assert g.sample(0.0) == (0, 0, 0)
    assert g.sample(1.0) == (255, 255, 255)


def test_generator_wrapper_no_len():
    out = io.StringIO()
    gen = (x for x in range(5))
    items = list(stillpoint(gen, stream=out))
    assert items == list(range(5))
