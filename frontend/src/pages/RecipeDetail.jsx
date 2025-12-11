import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ArrowLeft, Plus, Trash2, Save, ChefHat, DollarSign, PieChart, Users, Clock, AlertCircle } from 'lucide-react'
import axios from 'axios'
import { useState } from 'react'
import AddRecipeItemModal from '../components/recipes/AddRecipeItemModal'

export default function RecipeDetail() {
    const { id } = useParams()
    const queryClient = useQueryClient()
    const [isAddModalOpen, setIsAddModalOpen] = useState(false)

    // Fetch recipe details
    const { data: recipe, isLoading, error } = useQuery({
        queryKey: ['recipe', id],
        queryFn: async () => {
            const response = await axios.get(`/api/v1/recipes/${id}`)
            return response.data
        }
    })

    // Delete item mutation
    const deleteItemMutation = useMutation({
        mutationFn: async (itemId) => {
            await axios.delete(`/api/v1/recipes/${id}/items/${itemId}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipe', id])
        }
    })

    const handleDeleteItem = (itemId) => {
        if (window.confirm('¿Estás seguro de quitar este ingrediente?')) {
            deleteItemMutation.mutate(itemId)
        }
    }

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS'
        }).format(amount || 0)
    }

    if (isLoading) return (
        <div className="flex justify-center items-center min-h-[50vh]">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
    )

    if (error) return (
        <div className="text-center py-12 text-red-500">
            <AlertCircle className="w-12 h-12 mx-auto mb-4" />
            <p>Error al cargar la receta</p>
            <Link to="/recipes" className="text-primary hover:underline mt-4 block">Volver a recetas</Link>
        </div>
    )

    return (
        <div className="max-w-6xl mx-auto space-y-6 animate-fade-in pb-20">
            {/* Nav */}
            <div className="flex items-center gap-4">
                <Link to="/recipes" className="p-2 hover:bg-gray-100 rounded-full transition-colors text-gray-500">
                    <ArrowLeft className="w-5 h-5" />
                </Link>
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">{recipe.name}</h1>
                    <p className="text-sm text-gray-500">{recipe.recipe_type === 'final_dish' ? 'Plato Final' : recipe.recipe_type}</p>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="card p-4 border-l-4 border-blue-500">
                    <div className="flex items-center gap-3 mb-1">
                        <Users className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-500 font-medium">Rendimiento</span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{recipe.yield_quantity} <span className="text-sm font-normal text-gray-500">porciones</span></p>
                </div>

                <div className="card p-4 border-l-4 border-green-500">
                    <div className="flex items-center gap-3 mb-1">
                        <DollarSign className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-500 font-medium">Costo por Porción</span>
                    </div>
                    <p className="text-2xl font-bold text-green-700">{formatCurrency(recipe.cost_per_portion)}</p>
                </div>

                <div className="card p-4 border-l-4 border-purple-500">
                    <div className="flex items-center gap-3 mb-1">
                        <DollarSign className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-500 font-medium">Precio Sugerido</span>
                    </div>
                    <p className="text-2xl font-bold text-purple-700">{formatCurrency(recipe.suggested_price)}</p>
                </div>

                <div className="card p-4 border-l-4 border-amber-500">
                    <div className="flex items-center gap-3 mb-1">
                        <PieChart className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-500 font-medium">Margen Real</span>
                    </div>
                    <p className={`text-2xl font-bold ${recipe.target_margin > 0.35 ? 'text-green-600' : 'text-amber-600'}`}>
                        {Math.round((1 - (recipe.cost_per_portion / (recipe.suggested_price || 1))) * 100)}%
                    </p>
                    <p className="text-xs text-gray-400">Objetivo: {recipe.target_margin * 100}%</p>
                </div>
            </div>

            {/* Composition Table */}
            <div className="card">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                        <ChefHat className="w-5 h-5 text-gray-400" />
                        Composición (Ingredientes y Sub-recetas)
                    </h2>
                    <button
                        onClick={() => setIsAddModalOpen(true)}
                        className="btn btn-sm btn-outline flex items-center gap-2"
                    >
                        <Plus className="w-4 h-4" />
                        Agregar Item
                    </button>
                </div>

                {recipe.items.length === 0 ? (
                    <div className="text-center py-10 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                        <p className="text-gray-500 mb-2">Esta receta no tiene ingredientes aún.</p>
                        <button
                            onClick={() => setIsAddModalOpen(true)}
                            className="text-primary font-medium hover:underline"
                        >
                            Agregar el primer ingrediente
                        </button>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-gray-100 text-sm">
                                    <th className="text-left py-3 px-4 text-gray-500 font-medium">Ingrediente / Receta</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Cantidad</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Costo Total</th>
                                    <th className="text-center py-3 px-4 text-gray-500 font-medium">Notas</th>
                                    <th className="text-right py-3 px-4 text-gray-500 font-medium">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {recipe.items.map((item) => (
                                    <tr key={item.id} className="border-b border-gray-50 hover:bg-gray-50 text-sm">
                                        <td className="py-3 px-4">
                                            <div className="font-medium text-gray-900">
                                                {item.ingredient ? item.ingredient.name : item.child_recipe_name}
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                {item.ingredient ? 'Ingrediente' : 'Sub-receta'}
                                            </div>
                                        </td>
                                        <td className="py-3 px-4 text-right">
                                            {item.quantity} {item.unit_id} {/* TODO: Fetch unit name */}
                                        </td>
                                        <td className="py-3 px-4 text-right font-medium text-gray-900">
                                            {formatCurrency(item.item_cost)}
                                        </td>
                                        <td className="py-3 px-4 text-center text-gray-500 italic max-w-xs truncate">
                                            {item.notes || '-'}
                                        </td>
                                        <td className="py-3 px-4 text-right">
                                            <button
                                                onClick={() => handleDeleteItem(item.id)}
                                                className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                                                title="Eliminar"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                <tr className="bg-gray-50 font-bold">
                                    <td className="py-3 px-4 text-gray-900">Costo Total</td>
                                    <td colSpan="2" className="py-3 px-4 text-right text-gray-900">{formatCurrency(recipe.total_cost)}</td>
                                    <td colSpan="2"></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <AddRecipeItemModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                recipeId={parseInt(id)}
            />
        </div>
    )
}
