import { useState, useEffect } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { X, Save, AlertCircle } from 'lucide-react'
import axios from 'axios'
import PropTypes from 'prop-types'

export default function CreateSupplierModal({ isOpen, onClose, onSuccess, supplierToEdit = null }) {
    const queryClient = useQueryClient()
    const [serverError, setServerError] = useState('')
    const isEditing = !!supplierToEdit

    // Initial state
    const initialState = {
        name: '',
        contact_name: '',
        email: '',
        phone: '',
        address: '',
        tax_id: '',
        currency_code: 'ARS',
        payment_terms: '',
        lead_time_days: 1,
        minimum_order: 0,
        notes: ''
    }

    const [newItem, setNewItem] = useState(initialState)

    // Reset or populate form
    useEffect(() => {
        if (isOpen) {
            if (supplierToEdit) {
                setNewItem({
                    ...initialState,
                    ...supplierToEdit,
                    // Ensure numeric fields are numbers
                    lead_time_days: Number(supplierToEdit.lead_time_days || 1),
                    minimum_order: Number(supplierToEdit.minimum_order || 0)
                })
            } else {
                setNewItem(initialState)
            }
            setServerError('')
        }
    }, [isOpen, supplierToEdit])


    const mutation = useMutation({
        mutationFn: async (data) => {
            if (isEditing) {
                const response = await axios.put(`/api/v1/suppliers/${supplierToEdit.id}`, data)
                return response.data
            } else {
                const response = await axios.post('/api/v1/suppliers/', data)
                return response.data
            }
        },
        onSuccess: (data) => {
            queryClient.invalidateQueries(['suppliers'])
            setServerError('')
            if (onSuccess) {
                onSuccess(data)
            } else {
                onClose()
            }
        },
        onError: (error) => {
            setServerError(error.response?.data?.detail || 'Error al guardar proveedor')
        }
    })

    const handleSubmit = (e) => {
        e.preventDefault()
        mutation.mutate(newItem)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fade-in">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-2xl font-bold">{isEditing ? 'Editar Proveedor' : 'Nuevo Proveedor'}</h2>
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
                                <label className="label">Nombre Empresa</label>
                                <input
                                    required
                                    className="input w-full"
                                    value={newItem.name}
                                    onChange={e => setNewItem({ ...newItem, name: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">Contacto (Persona)</label>
                                <input
                                    className="input w-full"
                                    value={newItem.contact_name}
                                    onChange={e => setNewItem({ ...newItem, contact_name: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">Email</label>
                                <input
                                    type="email"
                                    className="input w-full"
                                    value={newItem.email}
                                    onChange={e => setNewItem({ ...newItem, email: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">Teléfono</label>
                                <input
                                    className="input w-full"
                                    value={newItem.phone}
                                    onChange={e => setNewItem({ ...newItem, phone: e.target.value })}
                                />
                            </div>
                            <div className="md:col-span-2">
                                <label className="label">Dirección</label>
                                <input
                                    className="input w-full"
                                    value={newItem.address}
                                    onChange={e => setNewItem({ ...newItem, address: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">CUIT / Tax ID</label>
                                <input
                                    className="input w-full"
                                    value={newItem.tax_id}
                                    onChange={e => setNewItem({ ...newItem, tax_id: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="label">Moneda Principal</label>
                                <select
                                    className="input w-full"
                                    value={newItem.currency_code}
                                    onChange={e => setNewItem({ ...newItem, currency_code: e.target.value })}
                                >
                                    <option value="ARS">ARS - Pesos Argentinos</option>
                                    <option value="USD">USD - Dólares</option>
                                    <option value="EUR">EUR - Euros</option>
                                </select>
                            </div>
                            <div>
                                <label className="label">Días de Entrega (Lead Time)</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    value={newItem.lead_time_days}
                                    onChange={e => setNewItem({ ...newItem, lead_time_days: parseInt(e.target.value) || 0 })}
                                />
                            </div>
                            <div>
                                <label className="label">Pedido Mínimo ($)</label>
                                <input
                                    type="number"
                                    className="input w-full"
                                    value={newItem.minimum_order}
                                    onChange={e => setNewItem({ ...newItem, minimum_order: parseFloat(e.target.value) || 0 })}
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
                                disabled={mutation.isPending}
                                className="btn btn-primary flex items-center gap-2"
                            >
                                <Save className="w-4 h-4" />
                                {mutation.isPending ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Guardar')}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

CreateSupplierModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onSuccess: PropTypes.func,
    supplierToEdit: PropTypes.object
}
