import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { X, Save, AlertCircle, Tag as TagIcon } from 'lucide-react'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import axios from 'axios'
import PropTypes from 'prop-types';

export default function CreateRecipeModal({ isOpen, onClose, recipeToEdit = null }) {
    const queryClient = useQueryClient()
    const [serverError, setServerError] = useState('')
    const [selectedTags, setSelectedTags] = useState([])
    const isEditing = !!recipeToEdit

    // Fetch available tags
    const { data: availableTags = [] } = useQuery({
        queryKey: ['tags'],
        queryFn: async () => {
            const response = await axios.get('/api/v1/tags/')
            return response.data
        }
    })

    const { register, handleSubmit, reset, formState: { errors } } = useForm({
        defaultValues: {
            name: '',
            description: '',
            recipe_type: 'final_dish',
            yield_quantity: 1,
            target_margin: 0.35,
            preparation_time: 0,
            shelf_life_hours: 24
        }
    })

    // Reset form when modal opens or recipeToEdit changes
    useEffect(() => {
        if (isOpen) {
            if (recipeToEdit) {
                reset({
                    name: recipeToEdit.name,
                    description: recipeToEdit.description || '',
                    recipe_type: recipeToEdit.recipe_type,
                    yield_quantity: recipeToEdit.yield_quantity,
                    target_margin: recipeToEdit.target_margin,
                    preparation_time: recipeToEdit.preparation_time,
                    shelf_life_hours: recipeToEdit.shelf_life_hours
                })
                // Set selected tags from recipe
                setSelectedTags(recipeToEdit.tags?.map(t => t.id) || [])
            } else {
                reset({
                    name: '',
                    description: '',
                    recipe_type: 'final_dish',
                    yield_quantity: 1,
                    target_margin: 0.35,
                    preparation_time: 0,
                    shelf_life_hours: 24
                })
                setSelectedTags([])
            }
            setServerError('')
        }
    }, [isOpen, recipeToEdit, reset])

    const mutation = useMutation({
        mutationFn: async (data) => {
            let recipe
            if (isEditing) {
                const response = await axios.put(`/api/v1/recipes/${recipeToEdit.id}`, data)
                recipe = response.data
            } else {
                const response = await axios.post('/api/v1/recipes/', data)
                recipe = response.data
            }

            // Handle tags assignment
            if (recipe && recipe.id) {
                // Get CURRENT tags from server (not from recipeToEdit which may be stale)
                let currentTagIds = []
                if (isEditing) {
                    try {
                        const currentRecipe = await axios.get(`/api/v1/recipes/${recipe.id}`)
                        currentTagIds = currentRecipe.data.tags?.map(t => t.id) || []
                    } catch (error) {
                        console.error('Error fetching current tags:', error)
                        currentTagIds = recipeToEdit?.tags?.map(t => t.id) || []
                    }
                }

                // Tags to add (in selectedTags but not in current)
                const tagsToAdd = selectedTags.filter(id => !currentTagIds.includes(id))

                // Tags to remove (in current but not in selectedTags)
                const tagsToRemove = currentTagIds.filter(id => !selectedTags.includes(id))

                // Add new tags
                for (const tagId of tagsToAdd) {
                    await axios.post(`/api/v1/recipes/${recipe.id}/tags/${tagId}`)
                }

                // Remove unselected tags
                for (const tagId of tagsToRemove) {
                    await axios.delete(`/api/v1/recipes/${recipe.id}/tags/${tagId}`)
                }
            }

            return recipe
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['recipes'])
            reset()
            setSelectedTags([])
            onClose()
            setServerError('')
        },
        onError: (error) => {
            setServerError(error.response?.data?.detail || 'Error al guardar la receta')
        }
    })

    const onSubmit = (data) => {
        setServerError('')
        mutation.mutate({
            ...data,
            yield_quantity: parseFloat(data.yield_quantity),
            target_margin: parseFloat(data.target_margin),
            preparation_time: parseInt(data.preparation_time),
            shelf_life_hours: parseInt(data.shelf_life_hours)
        })
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between p-6 border-b border-gray-100">
                    <h2 className="text-xl font-bold text-gray-900">{isEditing ? 'Editar Receta' : 'Nueva Receta'}</h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                    >
                        <X className="w-5 h-5 text-gray-500" />
                    </button>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
                    {serverError && (
                        <div className="p-4 bg-red-50 text-red-700 rounded-xl flex items-center gap-2">
                            <AlertCircle className="w-5 h-5 flex-shrink-0" />
                            <p>{serverError}</p>
                        </div>
                    )}

                    <div className="space-y-4">
                        {/* Nombre y Tipo */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Nombre de la Receta</label>
                                <input
                                    type="text"
                                    className={`input w-full ${errors.name ? 'border-red-300' : ''}`}
                                    placeholder="Ej: Lomo al Champignon"
                                    {...register('name', { required: 'El nombre es obligatorio' })}
                                />
                                {errors.name && <p className="text-xs text-red-500">{errors.name.message}</p>}
                            </div>

                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Tipo</label>
                                <select
                                    className="input w-full"
                                    {...register('recipe_type')}
                                >
                                    <option value="final_dish">Plato Final</option>
                                    <option value="sub_recipe">Sub-receta (Mise en place)</option>
                                    <option value="beverage">Bebida</option>
                                    <option value="dessert">Postre</option>
                                    <option value="appetizer">Entrada</option>
                                </select>
                            </div>
                        </div>

                        {/* Descripción */}
                        <div className="space-y-1">
                            <label className="text-sm font-medium text-gray-700">Descripción</label>
                            <textarea
                                className="input w-full h-24"
                                placeholder="Breve descripción del plato o preparación..."
                                {...register('description')}
                            />
                        </div>

                        {/* Métricas */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Rendimiento (Porciones)</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    className="input w-full"
                                    {...register('yield_quantity', { required: true, min: 0.1 })}
                                />
                            </div>

                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Margen Objetivo (0-1)</label>
                                <input
                                    type="number"
                                    step="0.05"
                                    max="0.99"
                                    className="input w-full"
                                    {...register('target_margin', { required: true, min: 0, max: 0.99 })}
                                />
                                <p className="text-xs text-gray-500">Ej: 0.35 para 35%</p>
                            </div>

                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Tiempo Prep. (min)</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    {...register('preparation_time')}
                                />
                            </div>

                            <div className="space-y-1">
                                <label className="text-sm font-medium text-gray-700">Vida Útil (hs)</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    {...register('shelf_life_hours')}
                                />
                            </div>
                        </div>

                        {/* Tags */}
                        <div className="space-y-1">
                            <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
                                <TagIcon className="w-4 h-4" />
                                Etiquetas
                            </label>
                            <div className="flex flex-wrap gap-2 p-3 border border-gray-200 rounded-lg min-h-[60px]">
                                {availableTags.length > 0 ? (
                                    availableTags.map(tag => (
                                        <button
                                            key={tag.id}
                                            type="button"
                                            onClick={() => {
                                                setSelectedTags(prev =>
                                                    prev.includes(tag.id)
                                                        ? prev.filter(id => id !== tag.id)
                                                        : [...prev, tag.id]
                                                )
                                            }}
                                            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${selectedTags.includes(tag.id)
                                                ? 'bg-primary-500 text-white'
                                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                                }`}
                                        >
                                            {tag.name}
                                        </button>
                                    ))
                                ) : (
                                    <p className="text-sm text-gray-500">No hay etiquetas disponibles</p>
                                )}
                            </div>
                            <p className="text-xs text-gray-500">Selecciona las etiquetas que aplican a esta receta</p>
                        </div>
                    </div>

                    <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn btn-ghost text-gray-600"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={mutation.isPending}
                            className="btn btn-primary flex items-center space-x-2"
                        >
                            <Save className="w-4 h-4" />
                            <span>{mutation.isPending ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear Receta')}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

CreateRecipeModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    recipeToEdit: PropTypes.object
};
