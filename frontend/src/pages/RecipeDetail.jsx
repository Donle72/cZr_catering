import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ArrowLeft, Plus, Trash2, Save, ChefHat, DollarSign, PieChart, Users, Clock, AlertCircle, Edit, Tag, X } from 'lucide-react'
import axios from 'axios'
import { useState } from 'react'
import AddRecipeItemModal from '../components/recipes/AddRecipeItemModal'

export default function RecipeDetail() {
    const { id } = useParams()
    const queryClient = useQueryClient()
    const [isAddModalOpen, setIsAddModalOpen] = useState(false)
    const [editingItem, setEditingItem] = useState(null)
    const [showTagSelector, setShowTagSelector] = useState(false)

    // Fetch recipe details
    const { data: recipe, isLoading, error } = useQuery({
        queryKey: ['recipe', id],
        queryFn: async () => {
            const response = await axios.get(`/api/v1/recipes/${id}`)
            return response.data
        }
    })

    // Fetch available tags
    const { data: availableTags = [] } = useQuery({
        queryKey: ['tags'],
        queryFn: async () => {
            const response = await axios.get('/api/v1/tags/')
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

    // Update item mutation
    const updateItemMutation = useMutation({
        mutationFn: async ({ itemId, data }) => {
            await axios.put(`/api/v1/recipes/${id}/items/${itemId}`, data)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipe', id])
            setEditingItem(null)
        }
    })

    // Add tag mutation
    const addTagMutation = useMutation({
        mutationFn: async (tagId) => {
            await axios.post(`/api/v1/recipes/${id}/tags/${tagId}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipe', id])
            queryClient.invalidateQueries(['recipes'])
        },
        onError: (error) => {
            alert('Error al agregar tag: ' + (error.response?.data?.detail?.message || error.message))
        }
    })

    // Remove tag mutation
    const removeTagMutation = useMutation({
        mutationFn: async (tagId) => {
            await axios.delete(`/api/v1/recipes/${id}/tags/${tagId}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipe', id])
            queryClient.invalidateQueries(['recipes'])
        },
        onError: (error) => {
            alert('Error al quitar tag: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleEditItem = (item) => {
        setEditingItem({
            id: item.id,
            quantity: item.quantity,
            notes: item.notes || ''
        })
    }

    const handleSaveEdit = () => {
        if (editingItem) {
            updateItemMutation.mutate({
                itemId: editingItem.id,
                data: {
                    quantity: parseFloat(editingItem.quantity),
                    notes: editingItem.notes
                }
            })
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

            {/* Tags Section */}
            <div className="card">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                        <Tag className="w-5 h-5 text-gray-400" />
                        Etiquetas
                    </h2>
                    <button
                        onClick={() => setShowTagSelector(!showTagSelector)}
                        className="btn btn-sm btn-outline flex items-center gap-2"
                    >
                        <Plus className="w-4 h-4" />
                        {showTagSelector ? 'Ocultar' : 'Agregar Tag'}
                    </button>
                </div>

                {/* Current Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                    {recipe.tags && recipe.tags.length > 0 ? (
                        recipe.tags.map(tag => (
                            <div
                                key={tag.id}
                                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-100 text-blue-800 border border-blue-200"
                            >
                                <span className="text-sm font-medium">{tag.name}</span>
                                <button
                                    onClick={() => removeTagMutation.mutate(tag.id)}
                                    className="hover:bg-blue-200 rounded-full p-0.5 transition-colors"
                                    title="Quitar tag"
                                >
                                    <X className="w-3 h-3" />
                                </button>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-500 text-sm">No hay etiquetas asignadas</p>
                    )}
                </div>

                {/* Tag Selector */}
                {showTagSelector && (
                    <div className="border-t border-gray-100 pt-4">
                        <p className="text-sm text-gray-600 mb-3">Selecciona una etiqueta para agregar:</p>
                        <div className="flex flex-wrap gap-2">
                            {availableTags
                                .filter(tag => !recipe.tags?.some(t => t.id === tag.id))
                                .map(tag => (
                                    <button
                                        key={tag.id}
                                        onClick={() => {
                                            addTagMutation.mutate(tag.id)
                                            setShowTagSelector(false)
                                        }}
                                        className="px-3 py-1.5 rounded-full text-sm font-medium bg-gray-100 text-gray-700 hover:bg-blue-100 hover:text-blue-800 border border-gray-200 hover:border-blue-200 transition-colors"
                                    >
                                        {tag.name}
                                    </button>
                                ))
                            }
                            {availableTags.filter(tag => !recipe.tags?.some(t => t.id === tag.id)).length === 0 && (
                                <p className="text-gray-500 text-sm">Todas las etiquetas ya están asignadas</p>
                            )}
                        </div>
                    </div>
                )}
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
                                            <div className="flex items-center justify-end gap-2">
                                                <button
                                                    onClick={() => handleEditItem(item)}
                                                    className="p-1 text-gray-400 hover:text-blue-500 transition-colors"
                                                    title="Editar"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDeleteItem(item.id)}
                                                    className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                                                    title="Eliminar"
                                                >
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
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

            {/* Edit Item Modal */}
            {editingItem && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md">
                        <h3 className="text-lg font-bold text-gray-900 mb-4">Editar Ingrediente</h3>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Cantidad
                                </label>
                                <input
                                    type="number"
                                    step="0.01"
                                    className="input w-full"
                                    value={editingItem.quantity}
                                    onChange={(e) => setEditingItem({
                                        ...editingItem,
                                        quantity: e.target.value
                                    })}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Notas (opcional)
                                </label>
                                <textarea
                                    className="input w-full"
                                    rows="3"
                                    value={editingItem.notes}
                                    onChange={(e) => setEditingItem({
                                        ...editingItem,
                                        notes: e.target.value
                                    })}
                                    placeholder="Ej: Picar finamente, reservar para decorar..."
                                />
                            </div>
                        </div>

                        <div className="flex gap-3 mt-6">
                            <button
                                onClick={() => setEditingItem(null)}
                                className="btn btn-outline flex-1"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={handleSaveEdit}
                                className="btn btn-primary flex-1"
                                disabled={updateItemMutation.isLoading}
                            >
                                {updateItemMutation.isLoading ? 'Guardando...' : 'Guardar'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
