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

                        <!-- <li class="nav-item">
                            <a class="nav-link" href="/entrada_notas">
                                <i class="fa fa-file-text" aria-hidden="true"></i> Entrada Notas Fiscais
                            </a>
                        </li> -->

                        <!-- <li class="nav-item">
                            <a class="nav-link" href="/conferencia">
                                <i class="fa fa-check" aria-hidden="true"></i> Conferência
                            </a>
                        </li> -->

                        <!-- <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="menuCarregamento" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="fa fa-file-text" aria-hidden="true"></i> Carregamentos
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="menuCarregamento">
                                <li><a class="dropdown-item" href="/carregamentos">Carregamentos</a></li>
                                <li><a class="dropdown-item" href="/main_carregamento">Nova Nota</a></li>
                                <li><a class="dropdown-item" href="/entrada_notas/relatorios">Relatórios</a></li>
                            </ul>
                        </li> -->
					</ul>
				</div>
    `
}
