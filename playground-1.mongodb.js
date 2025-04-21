// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use("futbol");

db.partidos.aggregate([
    {
      $match: {
        $or: [
          { local: "Rel" },
          { visitante: "Rel" }
        ]
      }
    },
    {
      $project: {
        esLocal: { $eq: ["$local", "Rel"] },
        golesRel: {
          $cond: [{ $eq: ["$local", "Rel"] }, "$resultado.local", "$resultado.visitante"]
        },
        golesRival: {
          $cond: [{ $eq: ["$local", "Rel"] }, "$resultado.visitante", "$resultado.local"]
        }
      }
    },
    {
      $project: {
        puntos: {
          $switch: {
            branches: [
              {
                case: { $gt: ["$golesRel", "$golesRival"] },
                then: 3
              },
              {
                case: { $eq: ["$golesRel", "$golesRival"] },
                then: 1
              }
            ],
            default: 0
          }
        }
      }
    },
    {
      $group: {
        _id: null,
        puntos_totales: { $sum: "$puntos" }
      }
    }
  ])


  db.partidos.aggregate([
    {
      $match: {
        $or: [
          { local: "Bar" },
          { visitante: "Bar" }
        ]
      }
    },
    {
      $project: {
        amarillasBar: {
          $cond: [
            { $eq: ["$local", "Bar"] },
            { $toInt: "$tarjetas.amarillas" },
            0
          ]
        },
        amarillasBarVisitante: {
          $cond: [
            { $eq: ["$visitante", "Bar"] },
            { $toInt: "$tarjetas.amarillas" },
            0
          ]
        }
      }
    },
    {
      $project: {
        totalAmarillas: { $add: ["$amarillasBar", "$amarillasBarVisitante"] }
      }
    },
    {
      $group: {
        _id: null,
        total: { $sum: "$totalAmarillas" },
        partidos: { $sum: 1 }
      }
    },
    {
      $project: {
        _id: 0,
        media_amarillas: { $divide: ["$total", "$partidos"] }
      }
    }
  ])

  db.partidos.aggregate([
    {
      $match: {
        $or: [
          { local: "Gra", visitante: "Vil" },
          { local: "Vil", visitante: "Gra" }
        ]
      }
    },
    {
      $project: {
        local: 1,
        visitante: 1,
        golesLocal: { $toInt: "$resultado.local" },
        golesVisitante: { $toInt: "$resultado.visitante" }
      }
    },
    {
      $project: {
        resultado: {
          $switch: {
            branches: [
              {
                case: {
                  $and: [
                    { $eq: ["$local", "Gra"] },
                    { $gt: ["$golesLocal", "$golesVisitante"] }
                  ]
                },
                then: "victoria_gra"
              },
              {
                case: {
                  $and: [
                    { $eq: ["$visitante", "Gra"] },
                    { $gt: ["$golesVisitante", "$golesLocal"] }
                  ]
                },
                then: "victoria_gra"
              },
              {
                case: {
                  $and: [
                    { $eq: ["$local", "Vil"] },
                    { $gt: ["$golesLocal", "$golesVisitante"] }
                  ]
                },
                then: "victoria_vil"
              },
              {
                case: {
                  $and: [
                    { $eq: ["$visitante", "Vil"] },
                    { $gt: ["$golesVisitante", "$golesLocal"] }
                  ]
                },
                then: "victoria_vil"
              }
            ],
            default: "empate"
          }
        }
      }
    },
    {
      $group: {
        _id: "$resultado",
        total: { $sum: 1 }
      }
    }
  ])
  
  
  
  