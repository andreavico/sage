"""
Cartesian Product Functorial Construction

AUTHORS:

 - Nicolas M. Thiery (2008-2010): initial revision and refactorization
"""
#*****************************************************************************
#  Copyright (C) 2010 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.lazy_import import lazy_import
from sage.categories.covariant_functorial_construction import CovariantFunctorialConstruction, CovariantConstructionCategory
from sage.categories.pushout import MultivariateConstructionFunctor

native_python_containers   = set([tuple, list, set, frozenset])

class CartesianProductFunctor(CovariantFunctorialConstruction, MultivariateConstructionFunctor):
    """
    A singleton class for the Cartesian product functor.

    EXAMPLES::

        sage: cartesian_product
        The cartesian_product functorial construction

    ``cartesian_product`` takes a finite collection of sets, and
    constructs the Cartesian product of those sets::

        sage: A = FiniteEnumeratedSet(['a','b','c'])
        sage: B = FiniteEnumeratedSet([1,2])
        sage: C = cartesian_product([A, B]); C
        The cartesian product of ({'a', 'b', 'c'}, {1, 2})
        sage: C.an_element()
        ('a', 1)
        sage: C.list()         # todo: not implemented
        [['a', 1], ['a', 2], ['b', 1], ['b', 2], ['c', 1], ['c', 2]]

    If those sets are endowed with more structure, say they are
    monoids (hence in the category `Monoids()`), then the result is
    automatically endowed with its natural monoid structure::

        sage: M = Monoids().example()
        sage: M
        An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
        sage: M.rename('M')
        sage: C = cartesian_product([M, ZZ, QQ])
        sage: C
        The cartesian product of (M, Integer Ring, Rational Field)
        sage: C.an_element()
        ('abcd', 1, 1/2)
        sage: C.an_element()^2
        ('abcdabcd', 1, 1/4)
        sage: C.category()
        Category of Cartesian products of monoids

        sage: Monoids().CartesianProducts()
        Category of Cartesian products of monoids

    The Cartesian product functor is covariant: if ``A`` is a
    subcategory of ``B``, then ``A.CartesianProducts()`` is a
    subcategory of ``B.CartesianProducts()`` (see also
    :class:`~sage.categories.covariant_functorial_construction.CovariantFunctorialConstruction`)::

        sage: C.categories()
        [Category of Cartesian products of monoids,
         Category of monoids,
         Category of Cartesian products of semigroups,
         Category of semigroups,
         Category of Cartesian products of unital magmas,
         Category of Cartesian products of magmas,
         Category of unital magmas,
         Category of magmas,
         Category of Cartesian products of sets,
         Category of sets, ...]

        [Category of Cartesian products of monoids,
         Category of monoids,
         Category of Cartesian products of semigroups,
         Category of semigroups,
         Category of Cartesian products of magmas,
         Category of unital magmas,
         Category of magmas,
         Category of Cartesian products of sets,
         Category of sets,
         Category of sets with partial maps,
         Category of objects]

    Hence, the role of ``Monoids().CartesianProducts()`` is solely to
    provide mathematical information and algorithms which are relevant
    to Cartesian product of monoids. For example, it specifies that
    the result is again a monoid, and that its multiplicative unit is
    the cartesian product of the units of the underlying sets::

        sage: C.one()
        ('', 1, 1)

    Those are implemented in the nested class
    :class:`Monoids.CartesianProducts
    <sage.categories.monoids.Monoids.CartesianProducts>` of
    ``Monoids(QQ)``. This nested class is itself a subclass of
    :class:`CartesianProductsCategory`.

    """
    _functor_name = "cartesian_product"
    _functor_category = "CartesianProducts"
    symbol = " (+) "

    def __init__(self):
        r"""
        Constructor. See :class:`CartesianProductFunctor` for details.

        TESTS::

            sage: from sage.categories.cartesian_product import CartesianProductFunctor
            sage: CartesianProductFunctor()
            The cartesian_product functorial construction
        """
        CovariantFunctorialConstruction.__init__(self)
        from sage.categories.sets_cat import Sets
        MultivariateConstructionFunctor.__init__(self, Sets(), Sets())

    def __call__(self, args):
        r"""
        Functorial construction application.

        This specializes the generic ``__call__`` from
        :class:`CovariantFunctorialConstruction` to:

        - handle the following plain Python containers as input:
          :class:`frozenset`, :class:`list`, :class:`set` and
          :class:`tuple`.

        - handle the empty list of factors.

        See the examples below.

        EXAMPLES::

            sage: cartesian_product([[0,1], ('a','b','c')])
            The cartesian product of ({0, 1}, {'a', 'b', 'c'})
            sage: _.category()
            Category of Cartesian products of finite enumerated sets

            sage: cartesian_product([set([0,1,2]), [0,1]])
            The cartesian product of ({0, 1, 2}, {0, 1})
            sage: _.category()
            Category of Cartesian products of sets

        Check that the empty product is handled correctly:

            sage: C = cartesian_product([])
            sage: C
            The cartesian product of ()
            sage: C.cardinality()
            1
            sage: C.an_element()
            ()
            sage: C.category()
            Category of Cartesian products of sets
        """
        if any(type(arg) in native_python_containers for arg in args):
            from sage.categories.sets_cat import Sets
            S = Sets()
            args = [S(a, enumerated_set=True) for a in args]
        elif not args:
            from sage.categories.sets_cat import Sets
            from sage.sets.cartesian_product import CartesianProduct
            return CartesianProduct((), Sets().CartesianProducts())

        return super(CartesianProductFunctor, self).__call__(args)

class CartesianProductsCategory(CovariantConstructionCategory):
    """
    An abstract base class for all ``CartesianProducts`` categories.

    TESTS::

        sage: C = Sets().CartesianProducts()
        sage: C
        Category of Cartesian products of sets
        sage: C.base_category()
        Category of sets
        sage: latex(C)
        \mathbf{CartesianProducts}(\mathbf{Sets})
    """

    _functor_category = "CartesianProducts"

    def _repr_object_names(self):
        """
        EXAMPLES::

            sage: ModulesWithBasis(QQ).CartesianProducts() # indirect doctest
            Category of Cartesian products of vector spaces with basis over Rational Field

        """
        # This method is only required for the capital `C`
        return "Cartesian products of %s"%(self.base_category()._repr_object_names())

    def CartesianProducts(self):
        """
        Return the category of (finite) Cartesian products of objects
        of ``self``.

        By associativity of Cartesian products, this is ``self`` (a Cartesian
        product of Cartesian products of `A`'s is a Cartesian product of
        `A`'s).

        EXAMPLES::

            sage: ModulesWithBasis(QQ).CartesianProducts().CartesianProducts()
            Category of Cartesian products of vector spaces with basis over Rational Field
        """
        return self

    def base_ring(self):
        """
        The base ring of a cartesian product is the base ring of the underlying category.

        EXAMPLES::

            sage: Algebras(ZZ).CartesianProducts().base_ring()
            Integer Ring
        """
        return self.base_category().base_ring()

# Moved to avoid circular imports
lazy_import('sage.categories.sets_cat', 'cartesian_product')
"""
The cartesian product functorial construction

See :class:`CartesianProductFunctor` for more information

EXAMPLES::

    sage: cartesian_product
    The cartesian_product functorial construction
"""

