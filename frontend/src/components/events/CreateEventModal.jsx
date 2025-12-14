import { useState } from 'react'
import { X, Calendar, Users, Briefcase } from 'lucide-react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

export default function CreateEventModal({ isOpen, onClose }) {
    const queryClient = useQueryClient()
    const [formData, setFormData] = useState({
        name: '',
        client_name: '',
        event_date: new Date().toISOString().split('T')[0],
        guest_count: 0
    })

    const createMutation = useMutation({
        mutationFn: async (newEvent) => {
            const res = await axios.post('/api/v1/events/', newEvent)
            return res.data
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['events'])
            onClose()
            setFormData({
                name: '',
                client_name: '',
                event_date: new Date().toISOString().split('T')[0],
                guest_count: 0
            })
        },
        onError: (error) => {
            alert('Error al crear evento: ' + (error.response?.data?.detail || error.message))
        }
    })

    const handleSubmit = (e) => {
        e.preventDefault()
        createMutation.mutate(formData)
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg transform transition-all scale-100">
                <div className="flex justify-between items-center p-6 border-b border-gray-100">
                    <h2 className="text-2xl font-bold text-gray-800">Nuevo Evento</h2>
                    <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                        <X className="w-5 h-5 text-gray-500" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    <div>
                        <label className="label">Nombre del Evento</label>
                        <div className="relative">
                            <input
                                required
                                className="input pl-10"
                                placeholder="Ej: Casamiento Pérez-García"
                                value={formData.name}
                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                            />
                            <Briefcase className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                        </div>
                    </div>

                    <div>
                        <label className="label">Cliente</label>
                        <input
                            required
                            className="input"
                            placeholder="Nombre del cliente o empresa"
                            value={formData.client_name}
                            onChange={e => setFormData({ ...formData, client_name: e.target.value })}
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="label">Fecha</label>
                            <div className="relative">
                                <input
                                    type="date"
                                    required
                                    className="input pl-10"
                                    value={formData.event_date}
                                    onChange={e => setFormData({ ...formData, event_date: e.target.value })}
                                />
                                <Calendar className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                            </div>
                        </div>
                        <div>
                            <label className="label">Invitados (Pax)</label>
                            <div className="relative">
                                <input
                                    type="number"
                                    min="1"
                                    required
                                    className="input pl-10"
                                    value={formData.guest_count}
                                    onChange={e => setFormData({ ...formData, guest_count: parseInt(e.target.value) })}
                                />
                                <Users className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                            </div>
                        </div>
                    </div>

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
                            disabled={createMutation.isPending}
                            className="btn btn-primary min-w-[120px]"
                        >
                            {createMutation.isPending ? 'Creando...' : 'Crear Evento'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
