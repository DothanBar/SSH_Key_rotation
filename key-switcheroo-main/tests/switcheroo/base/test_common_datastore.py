"""This module tests the features common to the abstract DataStore class.
This module utilizes the FileDataStore because it is the simplest one to use
"""
from pathlib import Path
from hamcrest import assert_that, equal_to
from tests.switcheroo.base.resources import Person, Figure, FigureSerializer
import tests.switcheroo.base.resources.module1 as module1  # pylint: disable="consider-using-from-import"
import tests.switcheroo.base.resources.module2 as module2  # pylint: disable="consider-using-from-import"
from switcheroo.base.data_store import FileDataStore


def test_ds_can_handle_different_classes(
    s3_datastore: FileDataStore, rand_person: Person, rand_figure: Figure
):
    s3_datastore.register_serializer(Figure, FigureSerializer())
    s3_datastore.publish(rand_person, rand_person.relative_loc)
    s3_datastore.publish(rand_figure, rand_figure.relative_loc)

    read_figure = s3_datastore.retrieve(rand_figure.relative_loc, Figure)
    read_person = s3_datastore.retrieve(rand_person.relative_loc, Person)

    assert_that(read_figure, equal_to(rand_figure))
    assert_that(read_person, equal_to(rand_person))


def test_ds_can_handle_diff_modules_same_class_name(s3_datastore: FileDataStore):
    s3_datastore.register_serializer(module1.SomeClass, module1.SomeClassSerializer())
    s3_datastore.register_serializer(module2.SomeClass, module2.SomeClassSerializer())

    mod1_loc = Path("mod1")
    mod2_loc = Path("mod2")

    mod1 = module1.SomeClass("Module1")
    mod2 = module2.SomeClass("Module2")

    s3_datastore.publish(mod1, mod1_loc)
    s3_datastore.publish(mod2, mod2_loc)

    retrieved_mod1 = s3_datastore.retrieve(mod1_loc, module1.SomeClass)
    retrieved_mod2 = s3_datastore.retrieve(mod2_loc, module2.SomeClass)
    assert retrieved_mod1 is not None
    assert retrieved_mod2 is not None
    assert_that(retrieved_mod1.value, equal_to(mod1.value))
    assert_that(retrieved_mod2.value, equal_to(mod2.value))
