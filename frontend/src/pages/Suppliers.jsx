import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Truck, DollarSign, Package, Edit, Trash2, Search, Mail } from 'lucide-react'
import axios from 'axios'
import CreateSupplierModal from '../components/suppliers/CreateSupplierModal'

export default function Suppliers() {
    const queryClient = useQueryClient()
    const [searchTerm, setSearchTerm] = useState('')
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [editingSupplier, setEditingSupplier] = useState(null)

    // Fetch suppliers
    const { data: suppliers, isLoading, error } = useQuery({
        queryKey: ['suppliers', searchTerm],
        queryFn: async () => {
            const params = new URLSearchParams()
            if (searchTerm) params.append('search', searchTerm)
            const response = await axios.get(`/api/v1/suppliers/?${params}`)
            return response.data
        }
    })

    const deleteMutation = useMutation({
        mutationFn: async (id) => {
            await axios.delete(`/api/v1/suppliers/${id}`)
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['suppliers'])
        },
        onError: (error) => {
            alert('Error al eliminar: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleEdit = (supplier) => {
        setEditingSupplier(supplier)
        setIsModalOpen(true)
    }

    const handleDelete = (id) => {
        if (window.confirm('¿Estás seguro de eliminar este proveedor?')) {
            deleteMutation.mutate(id)
        }
    }

    const handleCloseModal = () => {
        setIsModalOpen(false)
        setEditingSupplier(null)
    }

    const stats = suppliers ? {
        total: suppliers.length,
        // Placeholder stats logic
        totalProducts: 0,
        monthlySpend: 0
    } : { total: 0, totalProducts: 0, monthlySpend: 0 }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Proveedores</h1>
                    <p className="text-gray-600">Gestiona tus proveedores y listas de precios</p>
                </div>
                <button
                    type="button"
                    onClick={() => { setEditingSupplier(null); setIsModalOpen(true); }}
                    className="btn btn-primary flex items-center space-x-2"
                >
                    <Plus className="w-5 h-5" />
                    <span>Nuevo Proveedor</span>
                </button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-orange-600 font-medium mb-1">Total Proveedores</p>
                            <p className="text-3xl font-bold text-orange-900">{stats.total}</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
                            <Truck className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-green-600 font-medium mb-1">Gasto Mensual (Est)</p>
                            <p className="text-3xl font-bold text-green-900">$0</p>
                        </div>
                        <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                            <DollarSign className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-blue-600 font-medium mb-1">Productos</p>
                            <p className="text-3xl font-bold text-blue-900">0</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                            <Package className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Search */}
            <div className="card">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Buscar proveedor..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="input pl-10 w-full"
                    />
                </div>
            </div>

            {/* Suppliers List */}
            <div className="card overflow-hidden p-0">
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="inline-block w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-4 text-gray-600">Cargando proveedores...</p>
                    </div>
                ) : error ? (
                    <div className="p-12 text-center text-red-500">
                        Error al cargar proveedores
                    </div>
                ) : suppliers?.length === 0 ? (
                    <div className="p-12 text-center text-gray-500">
                        No se encontraron proveedores.
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-50 border-b border-gray-200">
                                <tr>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Empresa</th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Contacto</th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Detalles</th>
                                    <th className="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Acciones</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                                {suppliers.map((supplier) => (
                                    <tr key={supplier.id} className="hover:bg-gray-50 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="font-medium text-gray-900">{supplier.name}</div>
                                            <div className="text-xs text-gray-500">{supplier.tax_id || 'Sin CUIT'}</div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="text-sm text-gray-900">{supplier.contact_name || '-'}</div>
                                            <div className="flex items-center gap-2 mt-1">
                                                {supplier.email && <a href={`mailto:${supplier.email}`} className="text-xs text-blue-600 hover:underline flex items-center gap-1"><Mail className="w-3 h-3" /> {supplier.email}</a>}
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-600">
                                            <div>Lead Time: {supplier.lead_time_days} días</div>
                                            <div>Min Order: ${supplier.minimum_order}</div>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex items-center justify-end space-x-2">
                                                <button
                                                    onClick={() => handleEdit(supplier)}
                                                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                                                    title="Editar"
                                                >
                                                    <Edit className="w-4 h-4" />
                                                </button>
                                                <button
                                                    onClick={() => handleDelete(supplier.id)}
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
            </div>

            <CreateSupplierModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                supplierToEdit={editingSupplier}
                onSuccess={() => {
                    handleCloseModal()
                    queryClient.invalidateQueries(['suppliers'])
                }}
            />
        </div>
    )
}
