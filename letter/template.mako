%% -*- mode: latex; -*-
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{parskip}
\usepackage{ragged2e}
\usepackage[hidelinks]{hyperref}
\newcommand\margin{0.75in}
\usepackage[letterpaper,
            bindingoffset=0.2in,
            left=\margin,
            right=\margin,
            top=\margin,
            bottom=\margin,
            footskip=0.25in]{geometry}
\usepackage{graphicx}
\graphicspath{ {./} }

\newcommand{\email}{${contact['email']}}

\begin{document}
\pagenumbering{gobble}

\begin{flushleft}
${contact['name']}\\\
${contact['location']}\\\
${contact['phone']}\\\
\href{mailto:${contact['email']}}{${contact['email']}}\\\
% if 'date' in letter:
  ${letter['date']}
% else:
  \today
% endif
\end{flushleft}

\vspace{0.5cm}

\begin{flushleft}
% if 'recipient' in letter:
  ${letter['recipient']}\\\
% endif
% if 'company' in letter:
  ${letter['company']}\\\
% endif
% if 'address' in letter:
  ${letter['address']}\\\
% endif
% if 'location' in letter:
  ${letter['location']}\\\
% endif
\end{flushleft}
\vspace{1cm}

\raggedright
% if 'salutation' in letter:
  ${letter['salutation']}%
% elif 'recipient' in letter:
  Dear ${letter['recipient']},%
% else:
  Dear Hiring Manager,%
% endif

${letter.content}


\begin{flushleft}
Sincerely,\\\
% if signature_image:
  \vspace{3mm}
  \includegraphics[width=5cm]{${signature_image}}\\\
  \vspace{2mm}
% else:
  \vspace{2cm}
% endif
${contact['name']}
\end{flushleft}

\end{document}
