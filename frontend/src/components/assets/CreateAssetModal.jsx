import { useState, useEffect } from 'react'
import { X, Package } from 'lucide-react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

export default function CreateAssetModal({ isOpen, onClose, assetToEdit = null }) {
    const queryClient = useQueryClient()
    const isEditing = !!assetToEdit

    const [formData, setFormData] = useState({
        name: '',
        category: '',
        description: '',
        total_quantity: 1,
        purchase_price: 0,
        replacement_cost: 0,
        state: 'available',
        location: ''
    })

    // Reset or populate form
    useEffect(() => {
        if (isOpen) {
            if (assetToEdit) {
                setFormData({
                    name: assetToEdit.name || '',
                    category: assetToEdit.category || '',
                    description: assetToEdit.description || '',
                    total_quantity: assetToEdit.total_quantity || 1,
                    purchase_price: assetToEdit.purchase_price || 0,
                    replacement_cost: assetToEdit.replacement_cost || 0,
                    state: assetToEdit.state || 'available',
                    location: assetToEdit.location || ''
                })
            } else {
                setFormData({
                    name: '',
                    category: '',
                    description: '',
                    total_quantity: 1,
                    purchase_price: 0,
                    replacement_cost: 0,
                    state: 'available',
                    location: ''
                })
            }
        }
    }, [isOpen, assetToEdit])

    const mutation = useMutation({
        mutationFn: async (data) => {
            if (isEditing) {
                const res = await axios.put(`/api/v1/assets/${assetToEdit.id}`, data)
                return res.data
            } else {
                const res = await axios.post('/api/v1/assets/', data)
                return res.data
            }
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['assets'])
            onClose()
            setFormData({
                name: '',
                category: '',
                description: '',
                total_quantity: 1,
                purchase_price: 0,
                replacement_cost: 0,
                state: 'available',
                location: ''
            })
        },
        onError: (error) => {
            alert('Error al guardar activo: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleSubmit = (e) => {
        e.preventDefault()
        mutation.mutate(formData)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[100] p-4 backdrop-blur-sm animate-fade-in">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl transform transition-all scale-100 max-h-[90vh] overflow-y-auto">
                <div className="flex justify-between items-center p-6 border-b border-gray-100 sticky top-0 bg-white z-10">
                    <h2 className="text-2xl font-bold text-gray-800">{isEditing ? 'Editar Activo' : 'Nuevo Activo'}</h2>
                    <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <X className="w-5 h-5 text-gray-500" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {/* Name */}
                    <div>
                        <label className="label">Nombre del Activo *</label>
                        <div className="relative">
                            <input
                                required
                                className="input pl-10"
                                placeholder="Ej: Mesa redonda 1.5m"
                                value={formData.name}
                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                            />
                            <Package className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                        </div>
                    </div>

                    {/* Category */}
                    <div>
                        <label className="label">Categoría *</label>
                        <select
                            required
                            className="input"
                            value={formData.category}
                            onChange={e => setFormData({ ...formData, category: e.target.value })}
                        >
                            <option value="">Seleccionar categoría</option>
                            <option value="Mobiliario">Mobiliario</option>
                            <option value="Vajilla">Vajilla</option>
                            <option value="Equipamiento">Equipamiento</option>
                            <option value="Decoración">Decoración</option>
                            <option value="Cocina">Cocina</option>
                            <option value="Transporte">Transporte</option>
                            <option value="Otro">Otro</option>
                        </select>
                    </div>

                    {/* Description */}
                    <div>
                        <label className="label">Descripción</label>
                        <textarea
                            className="input"
                            rows="3"
                            placeholder="Descripción detallada del activo..."
                            value={formData.description}
                            onChange={e => setFormData({ ...formData, description: e.target.value })}
                        />
                    </div>

                    {/* Quantity and State */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="label">Cantidad *</label>
                            <input
                                type="number"
                                min="0"
                                required
                                className="input"
                                value={formData.total_quantity}
                                onChange={e => setFormData({ ...formData, total_quantity: parseInt(e.target.value) })}
                            />
                        </div>
                        <div>
                            <label className="label">Estado *</label>
                            <select
                                required
                                className="input"
                                value={formData.state}
                                onChange={e => setFormData({ ...formData, state: e.target.value })}
                            >
                                <option value="available">Disponible</option>
                                <option value="maintenance">Mantenimiento</option>
                                <option value="broken">Roto</option>
                                <option value="lost">Perdido</option>
                            </select>
                        </div>
                    </div>

                    {/* Prices */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="label">Precio de Compra</label>
                            <input
                                type="number"
                                min="0"
                                step="0.01"
                                className="input"
                                placeholder="0.00"
                                value={formData.purchase_price}
                                onChange={e => setFormData({ ...formData, purchase_price: parseFloat(e.target.value) || 0 })}
                            />
                        </div>
                        <div>
                            <label className="label">Costo de Reemplazo</label>
                            <input
                                type="number"
                                min="0"
                                step="0.01"
                                className="input"
                                placeholder="0.00"
                                value={formData.replacement_cost}
                                onChange={e => setFormData({ ...formData, replacement_cost: parseFloat(e.target.value) || 0 })}
                            />
                        </div>
                    </div>

                    {/* Location */}
                    <div>
                        <label className="label">Ubicación</label>
                        <input
                            className="input"
                            placeholder="Ej: Depósito A, Estante 3"
                            value={formData.location}
                            onChange={e => setFormData({ ...formData, location: e.target.value })}
                        />
                    </div>

                    {/* Actions */}
                    <div className="flex justify-end gap-3 mt-8 pt-4 border-t border-gray-50">
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={mutation.isPending}
                            className="btn btn-primary min-w-[120px]"
                        >
                            {mutation.isPending ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear Activo')}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
