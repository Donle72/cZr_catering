import { Plus, Truck, DollarSign, Package } from 'lucide-react'

export default function Suppliers() {
    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Proveedores</h1>
                    <p className="text-gray-600">Gestiona tus proveedores y listas de precios</p>
                </div>
                <button className="btn btn-primary flex items-center space-x-2">
                    <Plus className="w-5 h-5" />
                    <span>Nuevo Proveedor</span>
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-orange-600 font-medium mb-1">Total Proveedores</p>
                            <p className="text-3xl font-bold text-orange-900">23</p>
                        </div>
                        <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center">
                            <Truck className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-green-600 font-medium mb-1">Gasto Mensual</p>
                            <p className="text-3xl font-bold text-green-900">$18,450</p>
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
                            <p className="text-3xl font-bold text-blue-900">456</p>
                        </div>
                        <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                            <Package className="w-6 h-6 text-white" />
                        </div>
                    </div>
                </div>
            </div>

            <div className="card text-center py-12">
                <Truck className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-gray-900 mb-2">Módulo en Desarrollo</h3>
                <p className="text-gray-600 mb-6">
                    La gestión completa de proveedores estará disponible próximamente
                </p>
                <button className="btn btn-primary">
                    Agregar Primer Proveedor
                </button>
            </div>
        </div>
    )
}
