function renderizaSidebar (idSidebar){
    let sidebar = document.getElementById(idSidebar)
    sidebar.innerHTML = `
				<div class="scrollbar-inner sidebar-wrapper">
					<ul class="nav">
                        <li class="nav-item">
                        <a class="nav-link" href="/">
                            <i class="fas fa-comments"></i> Comunicação Interna
                        </a>
                        </li>
                        <li class="nav-item">
                        <a class="nav-link" href="/iscas">
                            <i class="fas fa-chart-line"></i> Relatório de Iscas
                        </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/envio_coletas">
                                <i class="fas fa-truck"></i> Download de Coletas
                            </a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link" href="/ctes">
                              <i class="fas fa-truck"></i>CT-e
                          </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/cidades_atendidas">
                                <i class="fas fa-city"></i> Cidades Atendidas
                            </a>
                        </li>
					</ul>
				</div>
    `
}

