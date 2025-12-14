import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { format, addDays, startOfWeek, endOfWeek } from 'date-fns';

const Production = () => {
    const [dateRange, setDateRange] = useState({
        start: startOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().split('T')[0],
        end: endOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().split('T')[0]
    });
    const [activeTab, setActiveTab] = useState('plan'); // 'plan' or 'shopping'

    // Fetch Production Plan
    const { data: planData, isLoading: isLoadingPlan } = useQuery({
        queryKey: ['productionPlan', dateRange],
        queryFn: async () => {
            const response = await axios.get(`/api/v1/production/plan?start_date=${dateRange.start}&end_date=${dateRange.end}`);
            return response.data;
        }
    });

    // Fetch Shopping List
    const { data: shoppingData, isLoading: isLoadingShopping } = useQuery({
        queryKey: ['shoppingList', dateRange],
        queryFn: async () => {
            const response = await axios.get(`/api/v1/production/shopping-list?start_date=${dateRange.start}&end_date=${dateRange.end}`);
            return response.data;
        },
        enabled: activeTab === 'shopping'
    });

    const handleDateChange = (e) => {
        const { name, value } = e.target;
        setDateRange(prev => ({ ...prev, [name]: value }));
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
                🍳 Producción y Compras
            </h1>

            {/* Date Controls */}
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow mb-6 flex gap-4 items-end">
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Desde</label>
                    <input
                        type="date"
                        name="start"
                        value={dateRange.start}
                        onChange={handleDateChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Hasta</label>
                    <input
                        type="date"
                        name="end"
                        value={dateRange.end}
                        onChange={handleDateChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>
                <button
                    onClick={() => {
                        setDateRange({
                            start: startOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().split('T')[0],
                            end: endOfWeek(new Date(), { weekStartsOn: 1 }).toISOString().split('T')[0]
                        })
                    }}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
                >
                    Esta Semana
                </button>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
                <button
                    className={`py-2 px-4 font-medium ${activeTab === 'plan' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                    onClick={() => setActiveTab('plan')}
                >
                    📅 Plan de Cocina (Prep Sheet)
                </button>
                <button
                    className={`py-2 px-4 font-medium ${activeTab === 'shopping' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
                    onClick={() => setActiveTab('shopping')}
                >
                    🛒 Lista de Compras
                </button>
            </div>

            {/* Content */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden min-h-[400px]">

                {/* PREP SHEET TAB */}
                {activeTab === 'plan' && (
                    <div className="p-6">
                        {isLoadingPlan ? (
                            <div className="text-center py-10">Cargando plan...</div>
                        ) : (
                            <>
                                <div className="mb-6">
                                    <h3 className="text-lg font-semibold mb-2">Eventos Incluidos:</h3>
                                    {planData?.events.length === 0 ? (
                                        <p className="text-gray-500 italic">No hay eventos confirmados en este rango.</p>
                                    ) : (
                                        <div className="flex flex-wrap gap-2">
                                            {planData?.events.map(ev => (
                                                <span key={ev.id} className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded dark:bg-blue-200 dark:text-blue-800">
                                                    {ev.date} - {ev.name} ({ev.guests} pax)
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    {/* Mise en Place (Sub-Recipes) */}
                                    <div>
                                        <h2 className="text-xl font-bold mb-4 flex items-center">
                                            <span className="mr-2">🥣</span> Mise en Place
                                        </h2>
                                        {planData?.sub_recipes.length === 0 ? (
                                            <p className="text-gray-500">Nada para pre-producir.</p>
                                        ) : (
                                            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
                                                {planData?.sub_recipes.map(item => (
                                                    <li key={item.id} className="py-3 flex justify-between items-center">
                                                        <div>
                                                            <p className="font-medium text-gray-900 dark:text-white">{item.name}</p>
                                                            <p className="text-sm text-gray-500">Para: {item.events.join(', ')}</p>
                                                        </div>
                                                        <span className="text-lg font-bold text-indigo-600">
                                                            {item.total_quantity.toFixed(1)} {item.unit}
                                                        </span>
                                                    </li>
                                                ))}
                                            </ul>
                                        )}
                                    </div>

                                    {/* Total Ingredients */}
                                    <div>
                                        <h2 className="text-xl font-bold mb-4 flex items-center">
                                            <span className="mr-2">🥕</span> Total Insumos
                                        </h2>
                                        {planData?.ingredients.length === 0 ? (
                                            <p className="text-gray-500">No se requieren insumos.</p>
                                        ) : (
                                            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
                                                {planData?.ingredients.map(item => (
                                                    <li key={item.id} className="py-3 flex justify-between items-center">
                                                        <div>
                                                            <p className="font-medium text-gray-900 dark:text-white">{item.name}</p>
                                                            <p className="text-xs text-gray-400">{item.events.length} eventos</p>
                                                        </div>
                                                        <div className="text-right">
                                                            <p className="font-bold text-gray-800 dark:text-gray-200">
                                                                {item.total_required.toFixed(2)} {item.unit}
                                                            </p>
                                                            <p className={`text-xs ${item.stock >= item.total_required ? 'text-green-600' : 'text-red-500'}`}>
                                                                Stock: {item.stock}
                                                            </p>
                                                        </div>
                                                    </li>
                                                ))}
                                            </ul>
                                        )}
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                )}

                {/* SHOPPING LIST TAB */}
                {activeTab === 'shopping' && (
                    <div className="p-6">
                        {isLoadingShopping ? (
                            <div className="text-center py-10">Generando lista de compras...</div>
                        ) : (
                            <>
                                <div className="flex justify-between items-center mb-6">
                                    <h2 className="text-xl font-bold text-gray-800 dark:text-white">
                                        Lista de Compras Sugerida
                                    </h2>
                                    <button
                                        onClick={() => window.print()}
                                        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded inline-flex items-center"
                                    >
                                        🖨️ Imprimir / PDF
                                    </button>
                                </div>

                                {shoppingData?.items.length === 0 ? (
                                    <div className="bg-green-50 border-l-4 border-green-400 p-4">
                                        <div className="flex">
                                            <div className="flex-shrink-0">
                                                ✅
                                            </div>
                                            <div className="ml-3">
                                                <p className="text-sm text-green-700">
                                                    ¡Todo cubierto! No hay compras necesarias para este período.
                                                    (El stock actual es suficiente)
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="overflow-x-auto">
                                        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                            <thead className="bg-gray-50 dark:bg-gray-700">
                                                <tr>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Insumo</th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Categoría</th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Necesidad Neta</th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Stock Actual</th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">A Comprar</th>
                                                </tr>
                                            </thead>
                                            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                                                {shoppingData?.items.map((item) => (
                                                    <tr key={item.id}>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                                            {item.name}
                                                            <span className="block text-xs text-gray-400">{item.sku}</span>
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                                            {item.category || '-'}
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                                            {item.total_required.toFixed(2)} {item.unit}
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                                            {item.stock} {item.unit}
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap">
                                                            <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                                                                {item.to_buy.toFixed(2)} {item.unit}
                                                            </span>
                                                        </td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Production;
