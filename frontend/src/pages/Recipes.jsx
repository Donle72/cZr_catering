import { useState } from 'react'
import { Plus, ChefHat, DollarSign, Clock, Search, TrendingUp, AlertCircle, Edit, Trash2 } from 'lucide-react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import { Link } from 'react-router-dom'
import CreateRecipeModal from '../components/recipes/CreateRecipeModal'
import Pagination from '../components/ui/Pagination'

export default function Recipes() {
    const queryClient = useQueryClient()
    const [searchTerm, setSearchTerm] = useState('')
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
    const [editingRecipe, setEditingRecipe] = useState(null)
    const [page, setPage] = useState(1)
    const [limit] = useState(10)

    // Fetch recipes
    const { data: recipesData, isLoading, error } = useQuery({
        queryKey: ['recipes', searchTerm, page, limit],
        queryFn: async () => {
            const params = new URLSearchParams()
            if (searchTerm) params.append('search', searchTerm)
            params.append('skip', (page - 1) * limit)
            params.append('limit', limit)

            const response = await axios.get('/api/v1/recipes/', { params })
            return response.data
        },
        keepPreviousData: true
    })

    const recipes = recipesData?.items || []
    const totalRecipes = recipesData?.total || 0
    const totalPages = Math.ceil(totalRecipes / limit)

    const deleteMutation = useMutation({
        mutationFn: async (id) => {
            await axios.delete(`/api/v1/recipes/${id}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipes'])
        },
        onError: (error) => {
            alert('Error al eliminar: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleEdit = (recipe) => {
        setEditingRecipe(recipe)
        setIsCreateModalOpen(true)
    }

    const handleDelete = (id) => {
        if (window.confirm('¿Estás seguro de eliminar esta receta?')) {
            deleteMutation.mutate(id)
        }
    }

    const handleCloseModal = () => {
        setIsCreateModalOpen(false)
        setEditingRecipe(null)
    }

    // Calculate stats
    // Note: avgCost here is only for the current page. Ideal would be a stats endpoint.
    const avgCost = recipes.length > 0
        ? recipes.reduce((acc, curr) => acc + curr.cost_per_portion, 0) / recipes.length
        : 0

    // Helper to format currency
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS'
        }).format(amount)
    }

    // Helper for recipe type badge
    const getTypeBadgeColor = (type) => {
        switch (type) {
            case 'final_dish': return 'bg-blue-100 text-blue-800 border-blue-200'
            case 'sub_recipe': return 'bg-purple-100 text-purple-800 border-purple-200'
            case 'beverage': return 'bg-amber-100 text-amber-800 border-amber-200'
            default: return 'bg-gray-100 text-gray-800 border-gray-200'
        }
    }

    const translateType = (type) => {
        switch (type) {
            case 'final_dish': return 'Plato Final'
            case 'sub_recipe': return 'Sub-receta'
            case 'beverage': return 'Bebida'
            case 'dessert': return 'Postre'
            case 'appetizer': return 'Entrada'
            default: return type
        }
    }

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Recetas</h1>
                    <p className="text-gray-600">Gestiona tus recetas con costeo automático e ingeniería de menú</p>
                </div>
                <button
                    className="btn btn-primary flex items-center space-x-2"
                    onClick={() => { setEditingRecipe(null); setIsCreateModalOpen(true); }}
                >
                    <Plus className="w-5 h-5" />
                    <span>Nueva Receta</span>
                </button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-purple-600 font-medium mb-1">Total Recetas</p>
                            <p className="text-3xl font-bold text-purple-900">{totalRecipes}</p>
                        </div>
                        <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/30">
                            <ChefHat className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-green-600 font-medium mb-1">Costo Promedio (Pág)</p>
                            <p className="text-3xl font-bold text-green-900">{formatCurrency(avgCost)}</p>
                        </div>
                        <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center shadow-lg shadow-green-500/30">
                            <DollarSign className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-blue-600 font-medium mb-1">Recetas Rentables (Pág)</p>
                            <p className="text-3xl font-bold text-blue-900">
                                {recipes.filter(r => r.suggested_price > r.cost_per_portion).length}
                            </p>
                        </div>
                        <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                            <TrendingUp className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters and List */}
            <div className="card">
                <div className="flex items-center gap-4 mb-6">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Buscar recetas..."
                            className="input pl-10 w-full"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    {/* Future filters can go here */}
                </div>

                {isLoading ? (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                        <p className="text-gray-500">Cargando recetas...</p>
                    </div>
                ) : error ? (
                    <div className="text-center py-12 text-red-500">
                        <AlertCircle className="w-12 h-12 mx-auto mb-4" />
                        <p>Error al cargar recetas</p>
                    </div>
                ) : recipes.length === 0 ? (
                    <div className="text-center py-12 text-gray-500 bg-gray-50 rounded-xl border border-gray-100 border-dashed">
                        <ChefHat className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                        <p>No se encontraron recetas</p>
                        <button
                            className="text-primary font-medium hover:underline mt-2"
                            onClick={() => { setEditingRecipe(null); setIsCreateModalOpen(true); }}
                        >
                            Crear tu primera receta
                        </button>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-100">
                                    <th className="text-left py-4 px-4 text-gray-500 font-medium">Nombre</th>
                                    <th className="text-left py-4 px-4 text-gray-500 font-medium">Tipo</th>
                                    <th className="text-left py-4 px-4 text-gray-500 font-medium">Tags</th>
                                    <th className="text-right py-4 px-4 text-gray-500 font-medium">Rendimiento</th>
                                    <th className="text-right py-4 px-4 text-gray-500 font-medium">Costo Porción</th>
                                    <th className="text-right py-4 px-4 text-gray-500 font-medium">Precio Sug.</th>
                                    <th className="text-right py-4 px-4 text-gray-500 font-medium">Margen</th>
                                    <th className="text-center py-4 px-4 text-gray-500 font-medium">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {recipes.map((recipe) => (
                                    <tr
                                        key={recipe.id}
                                        className="border-b border-gray-50 hover:bg-gray-50 transition-colors cursor-pointer group"
                                    >
                                        <td className="py-4 px-4">
                                            <div className="font-medium text-gray-900">{recipe.name}</div>
                                        </td>
                                        <td className="py-4 px-4">
                                            <span className={`badge ${getTypeBadgeColor(recipe.recipe_type)}`}>
                                                {translateType(recipe.recipe_type)}
                                            </span>
                                        </td>
                                        <td className="py-4 px-4">
                                            <div className="flex flex-wrap gap-1">
                                                {recipe.tags && recipe.tags.length > 0 ? (
                                                    recipe.tags.map(tag => (
                                                        <span
                                                            key={tag.id}
                                                            className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 border border-blue-200"
                                                            title={tag.description || tag.name}
                                                        >
                                                            {tag.name}
                                                        </span>
                                                    ))
                                                ) : (
                                                    <span className="text-gray-400 text-sm">-</span>
                                                )}
                                            </div>
                                        </td>
                                        <td className="py-4 px-4 text-right">
                                            {recipe.yield_quantity}
                                        </td>
                                        <td className="py-4 px-4 text-right font-medium text-gray-900">
                                            {formatCurrency(recipe.cost_per_portion)}
                                        </td>
                                        <td className="py-4 px-4 text-right text-gray-600">
                                            {formatCurrency(recipe.suggested_price)}
                                        </td>
                                        <td className="py-4 px-4 text-right">
                                            <span className="text-green-600 font-medium">
                                                {Math.round(recipe.target_margin * 100)}%
                                            </span>
                                        </td>
                                        <td className="py-4 px-4">
                                            <div className="flex items-center justify-center space-x-2">
                                                <Link
                                                    to={`/recipes/${recipe.id}`}
                                                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                                    title="Editar Receta"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </Link>
                                                <button
                                                    onClick={(e) => { e.stopPropagation(); handleDelete(recipe.id); }}
                                                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                                    title="Eliminar"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                <Pagination
                    currentPage={page}
                    totalPages={totalPages}
                    onPageChange={setPage}
                    hasNext={page < totalPages}
                    hasPrev={page > 1}
                />
            </div>

            <CreateRecipeModal
                isOpen={isCreateModalOpen}
                onClose={handleCloseModal}
                recipeToEdit={editingRecipe}
            />
        </div>
    )
}
