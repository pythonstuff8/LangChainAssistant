'use client';

import { ServiceFilter } from '@/lib/api';

interface ServiceSelectorProps {
    selected: ServiceFilter;
    onChange: (service: ServiceFilter) => void;
}

const services: { id: ServiceFilter; name: string; color: string }[] = [
    { id: 'all', name: 'All Services', color: 'from-purple-500 to-cyan-500' },
    { id: 'langchain', name: 'LangChain', color: 'from-green-500 to-emerald-500' },
    { id: 'langgraph', name: 'LangGraph', color: 'from-blue-500 to-indigo-500' },
    { id: 'langsmith', name: 'LangSmith', color: 'from-orange-500 to-yellow-500' },
];

export default function ServiceSelector({ selected, onChange }: ServiceSelectorProps) {
    return (
        <div className="flex flex-wrap gap-2 justify-center">
            {services.map((service) => (
                <button
                    key={service.id}
                    onClick={() => onChange(service.id)}
                    className={`
            service-pill relative overflow-hidden
            ${selected === service.id ? 'active' : ''}
          `}
                >
                    {selected === service.id && (
                        <span
                            className={`absolute inset-0 bg-gradient-to-r ${service.color} opacity-80`}
                        />
                    )}
                    <span className="relative z-10">{service.name}</span>
                </button>
            ))}
        </div>
    );
}
