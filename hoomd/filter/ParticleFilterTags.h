#ifndef __PARTICLE_FILTER_TAGS_H__
#define __PARTICLE_FILTER_TAGS_H__

#include "ParticleFilter.h"
#include <pybind11/numpy.h>

//! Select particles based on their tag
class PYBIND11_EXPORT ParticleFilterTags : public ParticleFilter
    {
    public:
        /** Args:
                tags: numpybind11array of tags to select
        */
        ParticleFilterTags(std::vector<unsigned int> tags)
            : ParticleFilter(), m_tags(tags) {}

        /** Args:
                tags: pybind11::array of tags to select
        */
        ParticleFilterTags(
            pybind11::array_t<unsigned int,pybind11::array::c_style> tags)
            : ParticleFilter()
            {
            unsigned int* tags_ptr = (unsigned int*)m_tags.data();
            m_tags.assign(tags_ptr, tags_ptr+m_tags.size());
            }
        virtual ~ParticleFilterTags() {}

        /*! \param tag Tag of the particle to check
            \returns true if \a m_tag_min <= \a tag <= \a m_tag_max
        */
        virtual std::vector<unsigned int> getSelectedTags(
                std::shared_ptr<SystemDefinition> sysdef) const
            {
            return m_tags;
            }
    protected:
        std::vector<unsigned int> m_tags;     //< Tags to use for filter

    };
#endif
