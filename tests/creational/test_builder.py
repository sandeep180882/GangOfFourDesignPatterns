import pytest

from patterns.creational.builder.pattern import QueryBuilder, QueryDirector


def test_fluent_build():
    q = (
        QueryBuilder().select("a", "b").from_("t").where("a > ?", 1).where("b = ?", 2)
        .order_by("a").limit(3).build()
    )
    assert q.sql == "SELECT a, b FROM t WHERE a > ? AND b = ? ORDER BY a ASC LIMIT 3"
    assert q.params == (1, 2)


def test_defaults_to_select_star():
    assert QueryBuilder().from_("t").build().sql == "SELECT * FROM t"


def test_validation():
    with pytest.raises(ValueError):
        QueryBuilder().select("a").build()
    with pytest.raises(ValueError):
        QueryBuilder().limit(0)


def test_director_recipe():
    q = QueryDirector().recent_orders(7, 2)
    assert q.sql.endswith("ORDER BY created_at DESC LIMIT 2")
    assert q.params == (7,)
