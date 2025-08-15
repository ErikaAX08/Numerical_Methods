export function Introduction() {
    const technologies = [
        {
            name: "Next.js 14",
            description: "Framework React con App Router",
            category: "Frontend",
            color: "from-blue-500 to-cyan-500",
        },
        {
            name: "TypeScript",
            description: "Tipado estático para JavaScript",
            category: "Language",
            color: "from-indigo-500 to-purple-500",
        },
        {
            name: "Tailwind CSS",
            description: "Framework CSS utility-first",
            category: "Styling",
            color: "from-teal-500 to-green-500",
        },
        {
            name: "Shadcn/ui",
            description: "Componentes UI accesibles",
            category: "UI Library",
            color: "from-orange-500 to-red-500",
        },
        {
            name: "React Hooks",
            description: "Gestión de estado moderno",
            category: "State",
            color: "from-pink-500 to-rose-500",
        },
        {
            name: "Vercel",
            description: "Plataforma de deployment",
            category: "Deployment",
            color: "from-violet-500 to-purple-500",
        },
    ]

    const team = [
        {
            name: "Erika Amastal Xochimitl",
            role: "Fulltack Developer",
            // description: "Especialista en React y diseño de interfaces",
            skills: ["React", "TypeScript", "UI/UX"],
            color: "from-pink-500 to-rose-500",
        },
        {
            name: "Guillermo Campos Salas",
            role: "Backend Developer",
            // description: "Arquitectura de software y APIs",
            skills: ["Node.js", "Database", "API Design"],
            color: "from-blue-500 to-indigo-500",
        },
        {
            name: "Iván Luna Martínez",
            role: "Applied Mathematics",
            // description: "Experta en métodos numéricos y algoritmos",
            skills: ["Numerical Analysis", "Algorithms", "Mathematics"],
            color: "from-emerald-500 to-teal-500",
        },
    ]

    return (
        <div className="space-y-32 mt-16 bg-white-60">
            <section className="text-center max-w-4xl mx-auto">
                <div className="text-slate-800 mb-6">
                    <h2 className="text-4xl font-bold mb-4">Explora el Mundo de los Métodos Numéricos</h2>
                </div>
                <p className="text-xl text-gray-700 leading-relaxed mb-8 font-medium">
                    Esta aplicación interactiva te permite explorar métodos numéricos utilizados en matemáticas aplicadas,
                    ingeniería y ciencias computacionales.
                </p>
                <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-100 to-blue-100 rounded-full border border-purple-200">
                    <span className="w-2 h-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-pulse"></span>
                    <p className="text-gray-600 font-medium">Selecciona una categoría para comenzar a explorar</p>
                </div>
            </section>

            <section>
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold text-slate-800 mb-4">
                        Stack Tecnológico
                    </h2>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                        Construido con tecnologías modernas para garantizar rendimiento, escalabilidad y mantenibilidad
                    </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {technologies.map((tech) => (
                        <div
                            key={tech.name}
                            className="group relative p-8 bg-white rounded-3xl border-2 border-gray-100 hover:border-transparent hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-500 hover:-translate-y-2 overflow-hidden"
                        >
                            <div
                                className={`absolute inset-0 bg-gradient-to-br ${tech.color} opacity-0 group-hover:opacity-10 transition-opacity duration-500`}
                            ></div>
                            <div className="relative z-10">
                                <div className="flex items-start justify-between mb-4">
                                    <div
                                        className={`w-12 h-12 bg-gradient-to-br ${tech.color} rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300`}
                                    >
                                        <span className="text-white font-bold text-lg">{tech.name[0]}</span>
                                    </div>
                                    <span
                                        className={`px-3 py-1 bg-gradient-to-r ${tech.color} text-white rounded-full text-xs font-bold shadow-md`}
                                    >
                                        {tech.category}
                                    </span>
                                </div>
                                <h3 className="font-bold text-xl text-gray-900 mb-3 group-hover:text-gray-700 transition-colors">
                                    {tech.name}
                                </h3>
                                <p className="text-gray-600 leading-relaxed">{tech.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            <section>
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold text-slate-800 mb-4">
                        Equipo de Desarrollo
                    </h2>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                        Un equipo multidisciplinario combinando experiencia en desarrollo de software y matemáticas aplicadas
                    </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
                    {team.map((member) => (
                        <div
                            key={member.name}
                            className="group relative p-8 bg-white rounded-3xl border-2 border-gray-100 hover:border-transparent hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 overflow-hidden"
                        >
                            <div
                                className={`absolute inset-0 bg-gradient-to-br ${member.color} opacity-0 group-hover:opacity-5 transition-opacity duration-500`}
                            ></div>
                            <div className="relative z-10">
                                <div className="flex items-start space-x-6">
                                    <div
                                        className={`w-20 h-20 bg-gradient-to-br ${member.color} rounded-3xl flex-shrink-0 flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform duration-300`}
                                    >
                                        <span className="text-2xl font-bold text-white">
                                            {member.name
                                                .split(" ")
                                                .map((n) => n[0])
                                                .join("")}
                                        </span>
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <h3 className="font-bold text-xl text-gray-900 mb-2 group-hover:text-gray-700 transition-colors">
                                            {member.name}
                                        </h3>
                                        <p
                                            className={`text-sm font-bold bg-gradient-to-r ${member.color} bg-clip-text text-transparent mb-3`}
                                        >
                                            {member.role}
                                        </p>
                                        <p className="text-gray-600 mb-4 leading-relaxed">{member.description}</p>
                                        <div className="flex flex-wrap gap-2">
                                            {member.skills.map((skill) => (
                                                <span
                                                    key={skill}
                                                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-medium hover:bg-gray-200 transition-colors"
                                                >
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    )
}
