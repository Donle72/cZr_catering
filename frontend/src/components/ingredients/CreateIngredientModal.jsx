import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { X, Save, AlertCircle } from 'lucide-react'
import axios from 'axios'
import PropTypes from 'prop-types'

export default function CreateIngredientModal({ isOpen, onClose, onSuccess }) {
    const queryClient = useQueryClient()
    const [serverError, setServerError] = useState('')

    // Initial state
    const initialState = {
        name: '',
        sku: '',
        category: 'Vegetales',
        purchase_unit_id: 1, // Default to KG
        usage_unit_id: 2,   // Default to G
        conversion_ratio: 1000,
        current_cost: 0,
        yield_factor: 1.0,
        tax_rate: 0.21,
        stock_quantity: 0,
        min_stock_threshold: 0
    }

    const [newItem, setNewItem] = useState(initialState)

    const categories = ['Carnes', 'Vegetales', 'Lácteos', 'Granos', 'Especias', 'Bebidas']

    const createMutation = useMutation({
        mutationFn: async (data) => {
            const response = await axios.post('/api/v1/ingredients/', data)
            return response.data
        },
        onSuccess: (data) => {
            queryClient.invalidateQueries(['ingredients'])
            queryClient.invalidateQueries(['ingredients_list']) // Also invalidate the list used in dropdowns
            setNewItem(initialState)
            setServerError('')
            if (onSuccess) {
                onSuccess(data)
            } else {
                onClose()
            }
        },
        onError: (error) => {
            setServerError(error.response?.data?.detail || 'Error al crear ingrediente')
        }
    })

    const handleSubmit = (e) => {
        e.preventDefault()
        createMutation.mutate(newItem)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-2xl font-bold">Nuevo Ingrediente</h2>
                        <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
                            <X className="w-5 h-5 text-gray-500" />
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        {serverError && (
                            <div className="p-3 bg-red-50 text-red-700 rounded-lg flex items-center gap-2">
                                <AlertCircle className="w-5 h-5" />
                                <p>{serverError}</p>
                            </div>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="label">Nombre</label>
                                <input
                                    required
                                    className="input w-full"
                                    value={newItem.name}
                                    onChange={e => setNewItem({ ...newItem, name: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">SKU</label>
                                <input
                                    className="input w-full"
                                    value={newItem.sku}
                                    onChange={e => setNewItem({ ...newItem, sku: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">Categoría</label>
                                <select
                                    className="input w-full"
                                    value={newItem.category}
                                    onChange={e => setNewItem({ ...newItem, category: e.target.value })}
                                >
                                    {categories.map(c => <option key={c} value={c}>{c}</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="label">Costo de Compra ($)</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    className="input w-full"
                                    value={newItem.current_cost}
                                    onChange={e => setNewItem({ ...newItem, current_cost: parseFloat(e.target.value) })}
                                />
                            </div>
                            <div>
                                <label className="label">Ratio Conversión</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    value={newItem.conversion_ratio}
                                    onChange={e => setNewItem({ ...newItem, conversion_ratio: parseFloat(e.target.value) })}
                                />
                                <p className="text-xs text-gray-500 mt-1">Ej: 1000 si compras Kg y usas gramos</p>
                            </div>
                            <div>
                                <label className="label">Factor Rendimiento (0-1)</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    max="1"
                                    className="input w-full"
                                    value={newItem.yield_factor}
                                    onChange={e => setNewItem({ ...newItem, yield_factor: parseFloat(e.target.value) })}
                                />
                            </div>
                            <div>
                                <label className="label">Stock Actual</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    value={newItem.stock_quantity}
                                    onChange={e => setNewItem({ ...newItem, stock_quantity: parseFloat(e.target.value) })}
                                />
                            </div>
                            <div>
                                <label className="label">Min. Stock Alerta</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    value={newItem.min_stock_threshold}
                                    onChange={e => setNewItem({ ...newItem, min_stock_threshold: parseFloat(e.target.value) })}
                                />
                            </div>
                        </div>
                        <div className="flex justify-end gap-3 mt-6">
                            <button
                                type="button"
                                onClick={onClose}
                                className="btn bg-gray-200 text-gray-800 hover:bg-gray-300"
                            >
                                Cancelar
                            </button>
                            <button
                                type="submit"
                                disabled={createMutation.isPending}
                                className="btn btn-primary flex items-center gap-2"
                            >
                                <Save className="w-4 h-4" />
                                {createMutation.isPending ? 'Guardando...' : 'Guardar'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

CreateIngredientModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onSuccess: PropTypes.func
}
