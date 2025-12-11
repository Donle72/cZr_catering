import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { X, Save, Search, AlertCircle, ChefHat, Carrot } from 'lucide-react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import PropTypes from 'prop-types'

export default function AddRecipeItemModal({ isOpen, onClose, recipeId }) {
    const queryClient = useQueryClient()
    const [serverError, setServerError] = useState('')
    const [activeTab, setActiveTab] = useState('ingredient') // 'ingredient' | 'recipe'

    // Form setup
    const { register, handleSubmit, reset, watch, setValue, formState: { errors } } = useForm({
        defaultValues: {
            ingredient_id: '',
            child_recipe_id: '',
            quantity: 1,
            unit_id: '',
            notes: ''
        }
    })

    // Fetch Ingredients (Simple full list for now, ideally paginated search)
    const { data: ingredientsData } = useQuery({
        queryKey: ['ingredients_list'],
        queryFn: async () => {
            const response = await axios.get('/api/v1/ingredients/?limit=100')
            return response.data.items
        },
        enabled: isOpen && activeTab === 'ingredient'
    })

    // Fetch Recipes (for sub-recipes)
    const { data: recipesData } = useQuery({
        queryKey: ['recipes_list'],
        queryFn: async () => {
            const response = await axios.get('/api/v1/recipes/?limit=100')
            return response.data.items.filter(r => r.id !== recipeId) // Exclude self
        },
        enabled: isOpen && activeTab === 'recipe'
    })

    // Fetch Units (Should be global or cached)
    const { data: units } = useQuery({
        queryKey: ['units'],
        queryFn: async () => {
            const response = await axios.get('/api/v1/units/')
            return response.data
        },
        enabled: isOpen
    })

    const addItemMutation = useMutation({
        mutationFn: async (data) => {
            const payload = {
                ...data,
                recipe_id: recipeId,
                quantity: parseFloat(data.quantity),
                unit_id: parseInt(data.unit_id),
                is_scalable: true
            }

            // Clean up based on tab
            if (activeTab === 'ingredient') {
                payload.ingredient_id = parseInt(payload.ingredient_id)
                delete payload.child_recipe_id
            } else {
                payload.child_recipe_id = parseInt(payload.child_recipe_id)
                delete payload.ingredient_id
            }

            const response = await axios.post(`/api/v1/recipes/${recipeId}/items`, payload)
            return response.data
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipe', recipeId])
            reset()
            onClose()
            setServerError('')
        },
        onError: (error) => {
            setServerError(error.response?.data?.detail || 'Error al agregar item')
        }
    })

    const onSubmit = (data) => {
        addItemMutation.mutate(data)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden">
                <div className="flex items-center justify-between p-6 border-b border-gray-100">
                    <h2 className="text-xl font-bold text-gray-900">Agregar a la Receta</h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                    >
                        <X className="w-5 h-5 text-gray-500" />
                    </button>
                </div>

                <div className="p-6">
                    {/* Tabs */}
                    <div className="flex p-1 bg-gray-100 rounded-xl mb-6">
                        <button
                            type="button"
                            className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2 ${activeTab === 'ingredient'
                                ? 'bg-white text-primary shadow-sm'
                                : 'text-gray-500 hover:text-gray-700'
                                }`}
                            onClick={() => setActiveTab('ingredient')}
                        >
                            <Carrot className="w-4 h-4" />
                            Ingrediente
                        </button>
                        <button
                            type="button"
                            className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2 ${activeTab === 'recipe'
                                ? 'bg-white text-purple-600 shadow-sm'
                                : 'text-gray-500 hover:text-gray-700'
                                }`}
                            onClick={() => setActiveTab('recipe')}
                        >
                            <ChefHat className="w-4 h-4" />
                            Sub-receta
                        </button>
                    </div>

                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                        {serverError && (
                            <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm flex items-center gap-2">
                                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                                <p>{serverError}</p>
                            </div>
                        )}

                        {/* Item Selector */}
                        <div className="space-y-1">
                            <label className="text-sm font-medium text-gray-700">
                                {activeTab === 'ingredient' ? 'Seleccionar Ingrediente' : 'Seleccionar Receta Base'}
                            </label>
                            <select
                                className="input w-full"
                                {...register(activeTab === 'ingredient' ? 'ingredient_id' : 'child_recipe_id', {
                                    required: 'Debes seleccionar un item'
                                })}
                            >
                                <option value="">Selecciona una opción...</option>
                                {activeTab === 'ingredient' ? (
                                    ingredientsData?.map(ing => (
                                        <option key={ing.id} value={ing.id}>
                                            {ing.name} ({ing.sku})
                                        </option>
                                    ))
                                ) : (
                                    recipesData?.map(r => (
                                        <option key={r.id} value={r.id}>
                                            {r.name}
                                        </option>
                                    ))
                                )}
                            </select>
                        </div>

                        {/* Quantity & Unit */}
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Cantidad</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    className="input w-full"
                                    placeholder="0.00"
                                    {...register('quantity', { required: true, min: 0.001 })}
                                />
                            </div>
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Unidad</label>
                                <select
                                    className="input w-full"
                                    {...register('unit_id', { required: true })}
                                >
                                    <option value="">Unidad...</option>
                                    {units?.map(u => (
                                        <option key={u.id} value={u.id}>
                                            {u.name} ({u.symbol})
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        {/* Notes */}
                        <div className="space-y-1">
                            <label className="text-sm font-medium text-gray-700">Notas (Opcional)</label>
                            <input
                                type="text"
                                className="input w-full"
                                placeholder="Ej: Cortado en cubos, sin piel..."
                                {...register('notes')}
                            />
                        </div>

                        <div className="pt-4 flex items-center justify-end gap-3">
                            <button
                                type="button"
                                onClick={onClose}
                                className="btn btn-ghost text-gray-600"
                            >
                                Cancelar
                            </button>
                            <button
                                type="submit"
                                disabled={addItemMutation.isPending}
                                className={`btn flex items-center space-x-2 ${activeTab === 'ingredient' ? 'btn-primary' : 'bg-purple-600 hover:bg-purple-700 text-white'
                                    }`}
                            >
                                <Save className="w-4 h-4" />
                                <span>{addItemMutation.isPending ? 'Agregando...' : 'Agregar Item'}</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

AddRecipeItemModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    recipeId: PropTypes.number.isRequired
}
